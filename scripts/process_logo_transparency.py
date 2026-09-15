from PIL import Image, ImageDraw

img = Image.open('media/logo/logo_conteelucre_inkscape_base.png').convert('RGBA')
w, h = img.size

# Inner circle center is w//2, h//2. Ring inner radius is around 0.44 * w
center = (w // 2, h // 2)
radius = int(w * 0.435)

# Create circular mask
mask = Image.new('L', (w, h), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill=255)

# Apply mask
output = Image.new('RGBA', (w, h), (0, 0, 0, 0))
output.paste(img, (0, 0), mask=mask)

# Save transparent circular badge
output.save('media/logo/logo_conteelucre_badge_transp.png')

# Also create a pure isolated vector-ready version:
# Make the light grey background pure white or transparent
pixels = output.load()
for x in range(w):
    for y in range(h):
        r, g, b, a = pixels[x, y]
        if a > 0:
            # If color is close to the off-white/light-grey background (#EFEFEF - #F5F5F5)
            if r > 230 and g > 230 and b > 230:
                pixels[x, y] = (255, 255, 255, 0)

output.save('media/logo/logo_conteelucre_isolated_transparent.png')
print('Successfully saved transparent logo variations!')
