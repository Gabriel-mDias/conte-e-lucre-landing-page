"""
Script de Processamento e Otimização de Mídias para Landing Pages.
- Varre media/logo/ e copia/otimiza SVGs para public/assets/logo/
- Gera favicon.svg automaticamente a partir do símbolo da marca
- Varre media/espaco/ (ou media/escritorio/) e converte para WebP/JPG com Lanczos e Unsharp Mask
- Varre media/equipe/ (ou media/colaboradores/) e converte retratos para WebP com preservação de canal alfa
- Varre media/video/ (ou media/movies/) e gera hero-poster.webp
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
PUBLIC_DIR = BASE_DIR / "public"
ASSETS_DIR = PUBLIC_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
COLAB_DIR = IMAGES_DIR / "colaboradores"
LOGO_DIR = ASSETS_DIR / "logo"
VIDEO_DIR = ASSETS_DIR / "video"

def ensure_dirs():
    for d in [PUBLIC_DIR, ASSETS_DIR, IMAGES_DIR, COLAB_DIR, LOGO_DIR, VIDEO_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def process_logos():
    print("[1/4] Processando e sincronizando logos SVG...")
    logo_src_dir = MEDIA_DIR / "logo"
    if not logo_src_dir.exists():
        print(f"  -> Diretorio {logo_src_dir} nao encontrado. Pulando.")
        return

    svg_files = list(logo_src_dir.glob("*.svg")) + list(logo_src_dir.glob("*.png"))
    if not svg_files:
        print(f"  -> Nenhum logo encontrado em {logo_src_dir}.")
        return

    fav_candidates = []
    for f in svg_files:
        dest = LOGO_DIR / f.name
        shutil.copy2(f, dest)
        sz_kb = dest.stat().st_size / 1024
        print(f"  -> Copiado: {f.name} ({sz_kb:.1f} KB)")
        if any(keyword in f.name.lower() for keyword in ["simbolo", "symbol", "icon", "logo"]):
            fav_candidates.append(f)

    # Copia o melhor candidato para favicon no root e em assets/logo
    primary_fav = fav_candidates[0] if fav_candidates else svg_files[0]
    shutil.copy2(primary_fav, PUBLIC_DIR / "favicon.svg")
    print(f"  -> Favicon sincronizado: {primary_fav.name} -> public/favicon.svg")

def process_espaco():
    print("\n[2/4] Processando fotos do espaco/arquitetura...")
    espaco_dir = MEDIA_DIR / "espaco"
    if not espaco_dir.exists():
        espaco_dir = MEDIA_DIR / "escritorio"
    
    if not espaco_dir.exists():
        print("  -> Nenhum diretorio de fotos do espaco encontrado. Pulando.")
        return

    extensions = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    photos = []
    for ext in extensions:
        photos.extend(espaco_dir.glob(ext))

    for p in photos:
        try:
            with Image.open(p) as im:
                im_rgb = im.convert("RGB")
                stem = p.stem.lower().replace(" ", "-")

                # Se a imagem tiver dimensao menor que 1200px, aplica upscale suave
                w, h = im_rgb.size
                if w < 1200:
                    scale = 2
                    im_up = im_rgb.resize((w * scale, h * scale), Image.Resampling.LANCZOS)
                    im_sharp = im_up.filter(ImageFilter.UnsharpMask(radius=2, percent=130, threshold=3))
                    enhancer = ImageEnhance.Contrast(im_sharp)
                    im_final = enhancer.enhance(1.04)
                else:
                    im_final = im_rgb

                out_webp = IMAGES_DIR / f"{stem}.webp"
                out_jpg = IMAGES_DIR / f"{stem}.jpg"

                im_final.save(out_webp, "WEBP", quality=88, method=6)
                im_final.save(out_jpg, "JPEG", quality=90, optimize=True)

                sz_webp = out_webp.stat().st_size / 1024
                print(f"  -> {stem}.webp gerado ({im_final.size[0]}x{im_final.size[1]}, {sz_webp:.1f} KB)")
        except Exception as e:
            print(f"  -> Erro ao processar {p.name}: {e}")

def process_equipe():
    print("\n[3/4] Processando fotos dos colaboradores/especialistas...")
    equipe_dir = MEDIA_DIR / "equipe"
    if not equipe_dir.exists():
        equipe_dir = MEDIA_DIR / "colaboradores"

    if not equipe_dir.exists():
        print("  -> Nenhum diretorio de equipe encontrado. Pulando.")
        return

    # Busca em subpastas ou diretamente
    candidates = list(equipe_dir.rglob("*.png")) + list(equipe_dir.rglob("*.webp")) + list(equipe_dir.rglob("*.jpg"))
    for c in candidates:
        if "cutout" in c.name.lower() or c.parent != equipe_dir or len(candidates) <= 10:
            try:
                with Image.open(c) as im:
                    im_rgba = im.convert("RGBA")
                    # Extrai o nome limpo
                    slug = c.stem.lower().replace("-cutout-web", "").replace("-cutout", "").replace(" ", "-")
                    # Se tiver numero ou pasta mae descritiva
                    if c.parent != equipe_dir:
                        slug = c.parent.name.lower().replace(" ", "-")

                    dest_webp = COLAB_DIR / f"{slug}.webp"
                    dest_png = COLAB_DIR / f"{slug}.png"

                    im_rgba.save(dest_webp, "WEBP", quality=92, method=6)
                    im_rgba.save(dest_png, "PNG", optimize=True)

                    sz_orig = c.stat().st_size / 1024
                    sz_webp = dest_webp.stat().st_size / 1024
                    red = ((1 - sz_webp / sz_orig) * 100) if sz_orig > 0 else 0
                    print(f"  -> {slug}.webp gerado ({sz_orig:.1f} KB -> {sz_webp:.1f} KB, -{red:.0f}%)")
            except Exception as e:
                print(f"  -> Erro ao processar {c.name}: {e}")

def process_video():
    print("\n[4/4] Sincronizando video de hero e gerando poster...")
    video_dir = MEDIA_DIR / "video"
    if not video_dir.exists():
        video_dir = MEDIA_DIR / "movies"

    if not video_dir.exists():
        print("  -> Nenhum diretorio de video encontrado. Pulando.")
        return

    mp4_files = list(video_dir.glob("*.mp4"))
    for v in mp4_files:
        dest = VIDEO_DIR / v.name
        shutil.copy2(v, dest)
        sz_mb = dest.stat().st_size / (1024 * 1024)
        print(f"  -> Video {v.name} copiado para {dest} ({sz_mb:.1f} MB)")

    # Gerar poster se existir foto de espaco
    poster_dest = VIDEO_DIR / "hero-poster.webp"
    if not poster_dest.exists():
        fotos = list(IMAGES_DIR.glob("*.webp")) + list(IMAGES_DIR.glob("*.jpg"))
        if fotos:
            with Image.open(fotos[0]) as im:
                im_rgb = im.convert("RGB")
                w, h = im_rgb.size
                target_h = int(w * 9 / 16)
                top = max(0, (h - target_h) // 3)
                cropped = im_rgb.crop((0, top, w, min(h, top + target_h)))
                cropped.save(poster_dest, "WEBP", quality=85)
                print(f"  -> Poster do Hero gerado em {poster_dest.name}")

if __name__ == "__main__":
    ensure_dirs()
    process_logos()
    process_espaco()
    process_equipe()
    process_video()
    print("\nProcessamento e sincronizacao de midias concluidos com exito!")
