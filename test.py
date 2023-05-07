from PIL import Image

# Charger l'image
image = Image.open('BUG.png')

# Remplacer le rouge (#ff0000) par le vert (#00ff00)
image = image.convert('RGBA')
blacklist = ((195, 220, 250), (199, 214, 233), (228, 234, 243))
region_no_bg = []
for item in image.getdata():
    pixel = (item[0], item[1], item[2])
    if pixel in blacklist:
        region_no_bg.append((255, 255, 255, item[3]))
    else:
        region_no_bg.append(item)

image.putdata(region_no_bg)

# Enregistrer l'image modifiée
image.show()
