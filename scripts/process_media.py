"""Pipeline deterministico de midias da landing page Conte & Lucre 2.0.

Requer Pillow e FFmpeg (direto ou via imageio-ffmpeg). Todas as saidas usadas
pelo HTML sao recriadas em ``public/assets`` sem deformar os originais.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "media"
ASSETS = ROOT / "public" / "assets"
LOGOS = ASSETS / "logo"
PEOPLE = ASSETS / "images" / "colaboradores"
POSTS = ASSETS / "images" / "posts"
VIDEO = ASSETS / "video"


def ensure_dirs() -> None:
    for directory in (LOGOS, PEOPLE, POSTS, VIDEO):
        directory.mkdir(parents=True, exist_ok=True)


def sharpen(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.UnsharpMask(radius=1.1, percent=105, threshold=3))


def responsive_image(source: Path, output_dir: Path, stem: str, widths: tuple[int, ...], alpha: bool = False) -> None:
    with Image.open(source) as opened:
        base = opened.convert("RGBA" if alpha else "RGB")
        generated: list[int] = []
        for width in widths:
            target_width = min(width, base.width)
            if target_width in generated:
                continue
            generated.append(target_width)
            target_height = round(base.height * target_width / base.width)
            resized = sharpen(base.resize((target_width, target_height), Image.Resampling.LANCZOS))
            resized.save(output_dir / f"{stem}-{target_width}.webp", "WEBP", quality=84, method=6, exact=alpha)

        fallback_width = min(max(widths), base.width)
        fallback_height = round(base.height * fallback_width / base.width)
        fallback = sharpen(base.resize((fallback_width, fallback_height), Image.Resampling.LANCZOS))
        extension = "png" if alpha else "jpg"
        output = output_dir / f"{stem}-{fallback_width}.{extension}"
        if alpha:
            fallback.save(output, "PNG", optimize=True, compress_level=9)
        else:
            fallback.save(output, "JPEG", quality=86, optimize=True, progressive=True)
        print(f"  -> {stem}: {', '.join(map(str, generated))} px + fallback {extension.upper()}")


def process_logos() -> None:
    print("[1/4] Logos")
    source_dir = MEDIA / "logo"
    for source in sorted(source_dir.glob("*")):
        if source.suffix.lower() in {".svg", ".png"}:
            shutil.copy2(source, LOGOS / source.name)
    primary = source_dir / "full_logo.svg"
    if primary.exists():
        shutil.copy2(primary, ROOT / "public" / "favicon.svg")

    # A assinatura usada na navegacao vem da faixa tipografica inferior da
    # marca oficial. O recorte proporcional mantem a geracao reproduzivel.
    raster = source_dir / "full_logo.png"
    if not raster.exists():
        raise FileNotFoundError(f"Marca oficial ausente: {raster}")
    with Image.open(raster) as opened:
        logo = opened.convert("RGBA")
        width, height = logo.size
        wordmark_band = logo.crop((0, round(height * 0.775), width, round(height * 0.925)))
        alpha_box = wordmark_band.getchannel("A").getbbox()
        if not alpha_box:
            raise RuntimeError("Nao foi possivel localizar a assinatura na marca oficial")
        left, top, right, bottom = alpha_box
        padding = max(6, round(height * 0.008))
        signature = wordmark_band.crop(
            (max(0, left - padding), max(0, top - padding), min(width, right + padding), min(wordmark_band.height, bottom + padding))
        )
        signature.save(LOGOS / "logo-signature.png", "PNG", optimize=True, compress_level=9)
        signature.save(LOGOS / "logo-signature.webp", "WEBP", quality=92, method=6, exact=True)
        print(f"  -> logo-signature: {signature.width}x{signature.height} px (PNG + WebP)")


def process_people() -> None:
    print("[2/4] Socios")
    jobs = (
        (MEDIA / "equipe" / "vanessa" / "vanessa_1.png", "vanessa", True),
        (MEDIA / "equipe" / "ruan" / "ruan_1.png", "ruan", True),
    )
    for source, stem, alpha in jobs:
        if not source.exists():
            raise FileNotFoundError(f"Midia obrigatoria ausente: {source}")
        responsive_image(source, PEOPLE, stem, (480, 720, 1080), alpha=alpha)

    with Image.open(MEDIA / "equipe" / "time_completo" / "time_completo.png") as opened:
        duo = opened.convert("RGBA")
        alpha_box = duo.getchannel("A").getbbox()
        if not alpha_box:
            raise RuntimeError("A composicao dos socios nao possui area visivel")
        duo = duo.crop(alpha_box)

        # Quadro 4:5 com margens de seguranca para rostos, ombros e maos. A
        # escala privilegia troncos e remove o vazio que existia no canvas.
        canvas_size = (1080, 1350)
        safe_size = (1030, 1310)
        duo.thumbnail(safe_size, Image.Resampling.LANCZOS)
        portrait_canvas = Image.new("RGB", canvas_size, "#dcebea")
        x = (canvas_size[0] - duo.width) // 2
        y = canvas_size[1] - duo.height
        portrait_canvas.paste(duo, (x, y), duo)
        portrait_canvas = sharpen(portrait_canvas)
        for target_width in (480, 720, 1080):
            target = portrait_canvas.resize((target_width, round(target_width * 5 / 4)), Image.Resampling.LANCZOS)
            target.save(PEOPLE / f"socios-{target_width}.webp", "WEBP", quality=84, method=6)
        portrait_canvas.save(PEOPLE / "socios-1080.jpg", "JPEG", quality=88, optimize=True, progressive=True)
        canvas = Image.new("RGB", (1200, 630), "#dcebea")
        ImageDraw.Draw(canvas).ellipse((735, -210, 1260, 315), outline="#8ac9c3", width=2)
        og_duo = duo.copy()
        og_duo.thumbnail((1050, 760), Image.Resampling.LANCZOS)
        canvas.paste(og_duo, ((1200 - og_duo.width) // 2, 630 - og_duo.height), og_duo)
        canvas.save(PEOPLE / "socios-og.jpg", "JPEG", quality=88, optimize=True, progressive=True)
        print("  -> socios: 4:5 reenquadrado (480/720/1080 WebP + JPG) e OG 1200x630")


def process_posts() -> None:
    print("[3/4] Posts")
    sources = sorted((MEDIA / "posts").glob("post */post_*.*"))
    sources = [item for item in sources if item.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    if len(sources) != 11:
        raise RuntimeError(f"Esperadas 11 paginas de posts; encontradas {len(sources)}")
    for source in sources:
        with Image.open(source) as opened:
            original = opened.convert("RGB")
            # Todas as paginas ficam completas dentro de um quadro 4:5. O
            # fundo neutro absorve pequenas diferencas de proporcao sem crop.
            normalized = Image.new("RGB", (1080, 1350), "#f4f1ec")
            contained = ImageOps.contain(original, normalized.size, Image.Resampling.LANCZOS)
            normalized.paste(contained, ((1080 - contained.width) // 2, (1350 - contained.height) // 2))
            normalized = sharpen(normalized)
            for target_width in (540, 1080):
                target = normalized.resize((target_width, round(target_width * 5 / 4)), Image.Resampling.LANCZOS)
                target.save(POSTS / f"{source.stem}-{target_width}.webp", "WEBP", quality=84, method=6)
            normalized.save(POSTS / f"{source.stem}-1080.jpg", "JPEG", quality=86, optimize=True, progressive=True)
            print(f"  -> {source.stem}: quadro 4:5 completo (540/1080 WebP + JPG)")


def ffmpeg_executable() -> str:
    system = shutil.which("ffmpeg")
    if system:
        return system
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as error:
        raise RuntimeError("Instale imageio-ffmpeg para gerar o poster da hero") from error


def process_video() -> None:
    print("[4/4] Video e poster")
    source = MEDIA / "video" / "hero_alternativa.mp4"
    if not source.exists():
        raise FileNotFoundError(f"Video obrigatorio ausente: {source}")
    ffmpeg = ffmpeg_executable()
    desktop = VIDEO / "hero-desktop.mp4"
    mobile = VIDEO / "hero-mobile.mp4"
    common = ["-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an"]
    subprocess.run([ffmpeg, "-y", "-i", str(source), "-vf", "scale=1280:720:flags=lanczos", *common, str(desktop)], check=True)
    subprocess.run(
        [ffmpeg, "-y", "-i", str(source), "-vf", "crop=ih*9/16:ih:(iw-ow)/2:0,scale=720:1280:flags=lanczos", *common, str(mobile)],
        check=True,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        for video, name, size in (
            (desktop, "hero-desktop-poster.webp", (1280, 720)),
            (mobile, "hero-mobile-poster.webp", (720, 1280)),
        ):
            frame = Path(temp_dir) / f"{name}.jpg"
            subprocess.run(
                [ffmpeg, "-y", "-ss", "00:00:01.000", "-i", str(video), "-frames:v", "1", "-q:v", "2", str(frame)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            with Image.open(frame) as opened:
                poster = ImageOps.fit(opened.convert("RGB"), size, Image.Resampling.LANCZOS)
                poster.save(VIDEO / name, "WEBP", quality=82, method=6)
    print("  -> hero desktop 1280x720 + mobile 720x1280, sem audio, faststart e posters")


def main() -> None:
    parser = argparse.ArgumentParser(description="Processa as midias da Conte & Lucre 2.0")
    parser.add_argument("--only", choices=("logos", "people", "posts", "video"))
    selected = parser.parse_args().only
    ensure_dirs()
    tasks = {"logos": process_logos, "people": process_people, "posts": process_posts, "video": process_video}
    if selected:
        tasks[selected]()
    else:
        for task in tasks.values():
            task()
    print("Processamento concluido.")


if __name__ == "__main__":
    main()
