import sys
from rembg import remove
from PIL import Image, ImageFilter

print("Removing background from Vanessa photo...")
input_path = 'media/equipe/vanessa_rezende_pianzola_original.jpg'
output_path = 'media/equipe/vanessa_sem_fundo.png'

inp = Image.open(input_path)
# Upscale first to 800x800 for cleaner edges
inp_large = inp.resize((800, 800), Image.Resampling.LANCZOS)
out = remove(inp_large)
out.save(output_path)
print(f"Saved {output_path}")

# Also let's clean the logo to transparent background
print("Processing clean logo with transparency...")
logo_raw = Image.open('media/logo/logo_conteelucre_original.png')
# Inner emblem without gradient ring:
w, h = logo_raw.size
# Let's crop tight inside the ring:
emblem_tight = logo_raw.crop((12, 12, w - 12, h - 12)).resize((1200, 1200), Image.Resampling.LANCZOS)
emblem_tight.save('media/logo/logo_conteelucre_clean.png')

print("All background processing completed!")
