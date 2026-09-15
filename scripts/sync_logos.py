import shutil
from pathlib import Path

src_svg = Path('media/logo/full_logo.svg')
dest_dir = Path('public/assets/logo')
dest_dir.mkdir(parents=True, exist_ok=True)

# 1. Copy original vector SVG
shutil.copy2(src_svg, dest_dir / 'full_logo.svg')
shutil.copy2(src_svg, dest_dir / 'logo-full.svg')
shutil.copy2(src_svg, dest_dir / 'logo-horizontal.svg')
shutil.copy2(src_svg, Path('public/favicon.svg'))
shutil.copy2(src_svg, dest_dir / 'favicon.svg')

# 2. Create white-variant for dark backgrounds (Hero, dark navbar, footer)
with open(src_svg, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace #737575 with #ffffff and #b3b2b2 with #94a3b8 / #cbd5e1 for crisp contrast
content_white = content.replace('#737575', '#ffffff').replace('#b3b2b2', '#94a3b8')

with open(dest_dir / 'full_logo_white.svg', 'w', encoding='utf-8') as f:
    f.write(content_white)

print("Saved full_logo.svg and full_logo_white.svg to public/assets/logo/!")
