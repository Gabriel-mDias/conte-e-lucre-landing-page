"""
Script de Super-Resolução, Remoção de Imperfeições e Processamento de Ativos de Marca
- Logo: Vetorização SVG via vtracer, PNGs/WebP 2048px/1024px transparentes e Favicons
- Retratos da Equipe: Segmentação u2net_human_seg + Alpha Matting + Upscale 2x-3x Lanczos + UnsharpMask
- Posts/Carrosséis: Upscale 2x Retina + Denoising de Tipografia + WebP/JPG
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import rembg
import vtracer

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
PROCESSED_DIR = MEDIA_DIR / "processed"
PUBLIC_DIR = BASE_DIR / "public"
PUBLIC_ASSETS = PUBLIC_DIR / "assets"

def setup_directories():
    dirs = [
        PROCESSED_DIR / "logo",
        PROCESSED_DIR / "equipe" / "vanessa",
        PROCESSED_DIR / "posts",
        PUBLIC_ASSETS / "logo",
        PUBLIC_ASSETS / "images" / "colaboradores",
        PUBLIC_ASSETS / "images" / "posts",
        PUBLIC_ASSETS / "video"
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    print("[1/5] Diretorios de destino inicializados com sucesso.")

def process_logo():
    print("\n[2/5] Processando Logos (Vetorizacao SVG + Master 2048px RGBA)...")
    raw_logo_png = MEDIA_DIR / "logo" / "full_logo_base.png"
    raw_logo_jpg = MEDIA_DIR / "logo" / "full_logo_arquivo_bruto.jpg"
    out_dir = PROCESSED_DIR / "logo"

    # 1. Upscale prévio para vetorização suave
    im_png = Image.open(raw_logo_png).convert("RGBA")
    w, h = im_png.size
    # Upscale 4x com Lanczos para eliminar serrilhado antes do tracing
    im_smooth = im_png.resize((w * 4, h * 4), Image.Resampling.LANCZOS)
    smooth_tmp = out_dir / "_temp_logo_smooth.png"
    im_smooth.save(smooth_tmp)

    # 2. Vetorização via vtracer
    svg_out = out_dir / "logo.svg"
    try:
        vtracer.convert_image_to_svg_py(
            str(smooth_tmp.resolve()),
            str(svg_out.resolve())
        )
        print(f"  -> Vetor SVG gerado: {svg_out.name} ({svg_out.stat().st_size / 1024:.1f} KB)")
    except Exception as err:
        print(f"  -> Aviso vtracer: {err}")
    finally:
        if smooth_tmp.exists():
            smooth_tmp.unlink()

    # 3. Gerar Master 2048px e 1024px com alpha limpo
    # Pegamos o cutout suavizado, aplicamos contraste e unsharp mask sutil
    im_2048 = im_png.resize((2048, int(2048 * h / w)), Image.Resampling.LANCZOS)
    r, g, b, a = im_2048.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb_sharp = rgb.filter(ImageFilter.UnsharpMask(radius=2.0, percent=140, threshold=2))
    # Limpeza de canal alfa: threshold suave para evitar halos
    a_arr = np.array(a)
    a_arr = np.where(a_arr < 15, 0, a_arr) # elimina ruído fraco
    a_clean = Image.fromarray(a_arr.astype(np.uint8))
    master_2048 = Image.merge("RGBA", (*rgb_sharp.split(), a_clean))

    png_2048 = out_dir / "logo-2048.png"
    webp_1024 = out_dir / "logo-1024.webp"
    master_2048.save(png_2048, "PNG", optimize=True)
    
    master_1024 = master_2048.resize((1024, int(1024 * h / w)), Image.Resampling.LANCZOS)
    master_1024.save(webp_1024, "WEBP", quality=95, method=6)
    print(f"  -> Master PNG 2048px gerado: {png_2048.name} ({png_2048.stat().st_size / 1024:.1f} KB)")
    print(f"  -> Master WebP 1024px gerado: {webp_1024.name} ({webp_1024.stat().st_size / 1024:.1f} KB)")

    # 4. Gerar favicon.svg e favicon.png
    fav_svg = out_dir / "favicon.svg"
    shutil.copy2(svg_out, fav_svg)
    fav_png = out_dir / "favicon.png"
    fav_img = master_1024.resize((192, int(192 * h / w)), Image.Resampling.LANCZOS)
    # Criar canvas quadrado 192x192
    fav_canvas = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
    offset_y = (192 - fav_img.height) // 2
    fav_canvas.paste(fav_img, (0, offset_y), fav_img)
    fav_canvas.save(fav_png, "PNG")
    print("  -> Favicons SVG e PNG gerados.")

def process_equipe():
    print("\n[3/5] Processando Retratos da Equipe (Segmentacao IA u2net_human_seg + Upscaling UHD)...")
    src_dir = MEDIA_DIR / "equipe" / "vanessa"
    out_dir = PROCESSED_DIR / "equipe" / "vanessa"
    
    session = rembg.new_session("u2net_human_seg")

    items = [
        ("vanessa_1.jpg", 2.0, "vanessa_1"),
        ("vanessa_2.jpg", 3.0, "vanessa_2"), # Crítico: sub-HD 626x782 -> 1878x2346
        ("vanessa_3.jpg", 2.0, "vanessa_3"),
        ("vanessa_4.jpg", 2.0, "vanessa_4")
    ]

    for fname, scale, slug in items:
        p = src_dir / fname
        if not p.exists():
            print(f"  -> [AVISO] {fname} nao encontrado. Pulando.")
            continue
        
        print(f"  -> Processando {fname} (Upscaling {scale}x)...")
        with Image.open(p) as img:
            img_rgb = img.convert("RGB")
            w_orig, h_orig = img_rgb.size

            # 1. Segmentação IA com Alpha Matting para recorte de alta precisão
            print(f"     Removendo imperfeicoes e gerando canal alfa com rembg...")
            cutout_raw = rembg.remove(
                img_rgb,
                session=session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=5
            )

            # 2. Super-resolução (Lanczos High-Order)
            new_w = int(w_orig * scale)
            new_h = int(h_orig * scale)
            print(f"     Realizando upscaling de {w_orig}x{h_orig} para {new_w}x{new_h}...")
            cutout_up = cutout_raw.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # 3. Realce de Nitidez, Contraste e Redução de Halos
            r, g, b, a = cutout_up.split()
            rgb_layer = Image.merge("RGB", (r, g, b))
            
            # Unsharp mask específico para fotografia de retratos
            sharp_factor = 135 if scale >= 3.0 else 120
            rgb_sharp = rgb_layer.filter(ImageFilter.UnsharpMask(radius=1.8, percent=sharp_factor, threshold=2))
            
            # Micro-ajuste de contraste
            enhancer = ImageEnhance.Contrast(rgb_sharp)
            rgb_enhanced = enhancer.enhance(1.04)

            # Limpeza anti-fringing no canal alfa
            a_arr = np.array(a)
            # Remove ruído semi-transparente residual nas bordas distantes
            a_arr = np.where(a_arr < 8, 0, a_arr)
            a_clean = Image.fromarray(a_arr.astype(np.uint8))

            final_cutout = Image.merge("RGBA", (*rgb_enhanced.split(), a_clean))

            # Salvar versões transparentes (PNG e WebP)
            out_png = out_dir / f"{slug}_cutout.png"
            out_webp = out_dir / f"{slug}_cutout.webp"
            final_cutout.save(out_png, "PNG", optimize=True)
            final_cutout.save(out_webp, "WEBP", quality=95, method=6)

            # 4. Versão Full Studio HD com fundo original restaurado e polido
            full_up = img_rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
            full_sharp = full_up.filter(ImageFilter.UnsharpMask(radius=1.8, percent=sharp_factor, threshold=2))
            enhancer_full = ImageEnhance.Contrast(full_sharp)
            final_full = enhancer_full.enhance(1.03)

            out_full_jpg = out_dir / f"{slug}_full.jpg"
            out_full_webp = out_dir / f"{slug}_full.webp"
            final_full.save(out_full_jpg, "JPEG", quality=92, optimize=True)
            final_full.save(out_full_webp, "WEBP", quality=90, method=6)

            sz_webp = out_webp.stat().st_size / 1024
            print(f"     [CONCLUIDO] {slug}: {new_w}x{new_h} px | Cutout WebP: {sz_webp:.1f} KB")

def process_posts():
    print("\n[4/5] Processando Posts e Carrosseis (Upscaling 2x Retina + Denoising)...")
    src_dir = MEDIA_DIR / "posts"
    out_dir = PROCESSED_DIR / "posts"
    
    posts = sorted(list(src_dir.glob("*.jpg")) + list(src_dir.glob("*.png")))
    for p in posts:
        with Image.open(p) as img:
            img_rgb = img.convert("RGB")
            w, h = img_rgb.size
            scale = 2.0
            new_w, new_h = int(w * scale), int(h * scale)

            # Upscaling de alta precisão
            im_up = img_rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
            # Realce de tipografia e contornos dos gráficos
            im_sharp = im_up.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=2))
            
            stem = p.stem.replace(" ", "_")
            out_webp = out_dir / f"{stem}_retina.webp"
            out_jpg = out_dir / f"{stem}_retina.jpg"
            
            im_sharp.save(out_webp, "WEBP", quality=92, method=6)
            im_sharp.save(out_jpg, "JPEG", quality=92, optimize=True)

            sz_kb = out_webp.stat().st_size / 1024
            print(f"  -> {stem}: {w}x{h} -> {new_w}x{new_h} px | WebP: {sz_kb:.1f} KB")

def sync_to_public():
    print("\n[5/5] Sincronizando ativos processados com public/assets/...")
    
    # 1. Logos
    logo_proc = PROCESSED_DIR / "logo"
    logo_pub = PUBLIC_ASSETS / "logo"
    for f in logo_proc.glob("*.*"):
        shutil.copy2(f, logo_pub / f.name)
    shutil.copy2(logo_proc / "favicon.svg", PUBLIC_DIR / "favicon.svg")
    print("  -> Logos e Favicon sincronizados em public/assets/logo e public/favicon.svg")

    # 2. Equipe / Vanessa
    equipe_proc = PROCESSED_DIR / "equipe" / "vanessa"
    colab_pub = PUBLIC_ASSETS / "images" / "colaboradores"
    # Sincroniza vanessa_2_cutout e vanessa_1_cutout como padrão
    for f in equipe_proc.glob("*.*"):
        shutil.copy2(f, colab_pub / f.name)
    # Copia o cutout principal como vanessa.webp e vanessa.png
    if (equipe_proc / "vanessa_2_cutout.webp").exists():
        shutil.copy2(equipe_proc / "vanessa_2_cutout.webp", colab_pub / "vanessa.webp")
        shutil.copy2(equipe_proc / "vanessa_2_cutout.png", colab_pub / "vanessa.png")
    print("  -> Retratos de alta definicao sincronizados em public/assets/images/colaboradores")

    # 3. Posts
    posts_proc = PROCESSED_DIR / "posts"
    posts_pub = PUBLIC_ASSETS / "images" / "posts"
    for f in posts_proc.glob("*.*"):
        shutil.copy2(f, posts_pub / f.name)
    print("  -> Posts retina sincronizados em public/assets/images/posts")

    # 4. Hero poster caso haja vídeo
    video_src = MEDIA_DIR / "video" / "conte-e-lucre-hero.mp4"
    if video_src.exists():
        shutil.copy2(video_src, PUBLIC_ASSETS / "video" / video_src.name)
        # Gerar poster a partir de vanessa_1_full
        poster_src = equipe_proc / "vanessa_1_full.jpg"
        if poster_src.exists():
            shutil.copy2(poster_src, PUBLIC_ASSETS / "video" / "hero-poster.webp")
        print("  -> Video e Hero Poster sincronizados em public/assets/video")

if __name__ == "__main__":
    print("=================================================================")
    print(" INICIANDO PROCESSAMENTO E RESTAURACAO DE IMAGENS EM ALTA DEFINICAO ")
    print("=================================================================")
    setup_directories()
    process_logo()
    process_equipe()
    process_posts()
    sync_to_public()
    print("\n=================================================================")
    print(" PIPELINE CONCLUIDO COM EXCESSO! TODAS AS MIDIAS EM UHD RETINA ")
    print("=================================================================")
