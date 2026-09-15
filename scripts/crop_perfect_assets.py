from PIL import Image, ImageFilter, ImageOps
import os

os.makedirs('media/logo', exist_ok=True)
os.makedirs('media/equipe', exist_ok=True)
os.makedirs('media/destaques', exist_ok=True)
os.makedirs('media/posts', exist_ok=True)
os.makedirs('media/espaco', exist_ok=True)

# 1. Instagram Profile Screenshot
img_ig = Image.open(r'C:\Users\gabri\.gemini\antigravity-ide\brain\cc8c8410-aee5-4438-8bb5-0e845edbcce0\profile_no_modal_1789421807426.png')

# Logo Emblem (inside ring: center 298, 181, radius ~72)
logo_crop = img_ig.crop((226, 109, 370, 253))
# Upscale 4x with Lanczos
logo_highres = logo_crop.resize((1440, 1440), Image.Resampling.LANCZOS)
logo_highres = logo_highres.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
logo_highres.save('media/logo/logo_conteelucre_hd.png')
logo_crop.save('media/logo/logo_conteelucre_original.png')

# Crop just the inner symbol & typography
# Symbol: top part of the logo circle
symbol_crop = img_ig.crop((250, 130, 346, 215)).resize((800, 700), Image.Resampling.LANCZOS)
symbol_crop.save('media/logo/simbolo_conteelucre_hd.png')

# 2. Highlights (Resultados, Gestão PJ, Propósito)
# Let's find each highlight center in the row around y=400
# Destaque 1: Resultados (~ x=245)
dest_res = img_ig.crop((202, 346, 290, 434)).resize((600, 600), Image.Resampling.LANCZOS)
dest_res.save('media/destaques/destaque_resultados_hd.png')

# Destaque 2: Gestão PJ (~ x=375)
dest_pj = img_ig.crop((332, 346, 420, 434)).resize((600, 600), Image.Resampling.LANCZOS)
dest_pj.save('media/destaques/destaque_gestao_pj_hd.png')

# Destaque 3: Propósito (~ x=505)
dest_prop = img_ig.crop((462, 346, 550, 434)).resize((600, 600), Image.Resampling.LANCZOS)
dest_prop.save('media/destaques/destaque_proposito_hd.png')

# 3. Posts & Feed
# Grid starts around y=575
# Post 1 (Left - Making-of Ensaio): x ~ 156 to 468, y ~ 575 to 887
post1 = img_ig.crop((156, 575, 468, 887)).resize((1200, 1200), Image.Resampling.LANCZOS)
post1.save('media/posts/post1_makingof_ensaio.png')

# Inside Post 1: The camera monitor showing Vanessa & Partner in corporate suits
# monitor screen: x ~ 230 to 400, y ~ 690 to 900
socios_screen = img_ig.crop((240, 695, 395, 885)).resize((800, 980), Image.Resampling.LANCZOS)
socios_screen = socios_screen.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=2))
socios_screen.save('media/equipe/socios_ensaio_executivo.png')

# Post 2 (Center - Vanessa "Casais que planejam, prosperam"): x ~ 472 to 784, y ~ 575 to 887
post2 = img_ig.crop((472, 575, 784, 887)).resize((1200, 1200), Image.Resampling.LANCZOS)
post2.save('media/posts/post2_casais_prosperam.png')

# Vanessa portrait from Post 2
vanessa_p2 = img_ig.crop((475, 575, 780, 800)).resize((900, 675), Image.Resampling.LANCZOS)
vanessa_p2.save('media/equipe/vanessa_portrait_ensaio.png')

# Post 3 (Right - Tipografia "Você está progredindo? ou só movimentando?"): x ~ 788 to 1100, y ~ 575 to 887
post3 = img_ig.crop((788, 575, 1100, 887)).resize((1200, 1200), Image.Resampling.LANCZOS)
post3.save('media/posts/post3_progredindo_movimentando.png')

# 4. Linktree Profile Picture (Vanessa Rezende Pianzola)
img_lt = Image.open(r'C:\Users\gabri\.gemini\antigravity-ide\brain\cc8c8410-aee5-4438-8bb5-0e845edbcce0\linktree_page_1789422600941.png')
# Find avatar circle in linktree: roughly x=572 to 672, y=148 to 248
vanessa_avatar = img_lt.crop((572, 148, 672, 248)).resize((600, 600), Image.Resampling.LANCZOS)
vanessa_avatar = vanessa_avatar.filter(ImageFilter.UnsharpMask(radius=2, percent=130, threshold=2))
vanessa_avatar.save('media/equipe/vanessa_pianzola_avatar.png')

print("High resolution media assets extracted and upscaled successfully!")
