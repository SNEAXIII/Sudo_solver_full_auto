from PIL import Image

# Charger l'image
image = Image.open('BUG.png')

# Remplacer le rouge (#ff0000) par le vert (#00ff00)
image = image.convert('RGBA')
new_data = []
for item in image.getdata():
    if item[0] == 61 and item[1] == 108 and item[2] == 223:
        new_data.append((0, 255, 0, item[3]))
    else:
        new_data.append(item)

image.putdata(new_data)

# Enregistrer l'image modifiée
image.save('mon_image_modifiee.png')