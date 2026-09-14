from PIL import Image

img = Image.open('media/equipe/socios_ensaio_executivo.png')
w, h = img.size
# Crop inner screen area:
# left ~ 120, top ~ 0, right ~ 750, bottom ~ 760
cropped = img.crop((120, 10, 760, 750)).resize((1000, 1150), Image.Resampling.LANCZOS)
cropped.save('media/equipe/socios_posicionamento_executivo.png')
print('Saved media/equipe/socios_posicionamento_executivo.png')
