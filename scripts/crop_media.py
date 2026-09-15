from PIL import Image, ImageEnhance, ImageFilter
import os

os.makedirs('media/logo', exist_ok=True)
os.makedirs('media/equipe', exist_ok=True)
os.makedirs('media/destaques', exist_ok=True)
os.makedirs('media/posts', exist_ok=True)

# 1. Open Instagram Profile Screenshot
img_ig = Image.open(r'C:\Users\gabri\.gemini\antigravity-ide\brain\cc8c8410-aee5-4438-8bb5-0e845edbcce0\profile_no_modal_1789421807426.png')
w, h = img_ig.size
print(f"IG Screenshot size: {w}x{h}")

# The logo is the circle on the upper left
# In 1249x917 image:
# Avatar bounding box is roughly: left=170, top=105, right=310, bottom=280
logo_crop = img_ig.crop((170, 105, 310, 280))
logo_crop.save('media/logo/logo_raw_crop.png')

# Inside the gradient ring, let's crop just the brand emblem
# Let's crop tight around the logo emblem & text: left=180, top=115, right=300, bottom=270
emblem_crop = img_ig.crop((182, 117, 298, 268))
emblem_crop.save('media/logo/logo_emblem.png')

# 2. Highlights
# Resultados: ~ 160 to 235, 345 to 445
h_res = img_ig.crop((160, 345, 235, 450))
h_res.save('media/destaques/destaque_resultados.png')

# Gestão PJ: ~ 265 to 340, 345 to 450
h_pj = img_ig.crop((265, 345, 340, 450))
h_pj.save('media/destaques/destaque_gestao_pj.png')

# Propósito: ~ 368 to 445, 345 to 450
h_prop = img_ig.crop((368, 345, 445, 450))
h_prop.save('media/destaques/destaque_proposito.png')

# 3. Posts & Photos
# Post 1: Making-of partners on camera screen
post1 = img_ig.crop((125, 570, 375, 917))
post1.save('media/posts/post_ensaio_socios.png')

# The camera screen inside Post 1 showing the partners:
# Coordinates roughly: left=180, top=670, right=320, bottom=860
socios_screen = img_ig.crop((175, 670, 325, 860))
socios_screen.save('media/equipe/socios_ensaio.png')

# Post 2: Vanessa Rezende Pianzola
post2 = img_ig.crop((375, 570, 625, 917))
post2.save('media/posts/post_vanessa_casais.png')
# Vanessa portrait without text overlay:
vanessa_portrait = img_ig.crop((380, 570, 620, 770))
vanessa_portrait.save('media/equipe/vanessa_portrait.png')

# Post 3: Typography "Você está progredindo? ou só movimentando?"
post3 = img_ig.crop((625, 570, 875, 917))
post3.save('media/posts/post_progredindo.png')

# 4. Linktree Profile Picture
img_lt = Image.open(r'C:\Users\gabri\.gemini\antigravity-ide\brain\cc8c8410-aee5-4438-8bb5-0e845edbcce0\linktree_page_1789422600941.png')
w_lt, h_lt = img_lt.size
print(f"Linktree size: {w_lt}x{h_lt}")
# Profile circle is centered around x=580, y=200 in the 1278x944 screenshot
# Let's crop roughly x=540 to 680, y=140 to 260
vanessa_lt = img_lt.crop((560, 145, 665, 255))
vanessa_lt.save('media/equipe/vanessa_linktree_avatar.png')

print("All base crops saved successfully!")
