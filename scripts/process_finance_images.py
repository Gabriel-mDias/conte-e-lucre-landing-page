import shutil
from pathlib import Path
from PIL import Image

dest_dir = Path('public/assets/images')
dest_dir.mkdir(parents=True, exist_ok=True)

img1_src = Path(r'C:\Users\gabri\.gemini\antigravity-ide\brain\cc8c8410-aee5-4438-8bb5-0e845edbcce0\executive_finance_office_1789431474841.jpg')
img2_src = Path(r'C:\Users\gabri\.gemini\antigravity-ide\brain\cc8c8410-aee5-4438-8bb5-0e845edbcce0\financial_growth_detail_1789431538200.jpg')

# Process image 1
im1 = Image.open(img1_src)
im1.save(dest_dir / 'espaco-1.jpg', 'JPEG', quality=95)
im1.save(dest_dir / 'espaco-1.webp', 'WEBP', quality=90)
print('Saved espaco-1.jpg and espaco-1.webp')

# Process image 2
im2 = Image.open(img2_src)
im2.save(dest_dir / 'espaco-2.jpg', 'JPEG', quality=95)
im2.save(dest_dir / 'espaco-2.webp', 'WEBP', quality=90)
print('Saved espaco-2.jpg and espaco-2.webp')
