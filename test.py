from PIL import ImageGrab, Image

longueur_case = 54

screen = ImageGrab.grab((386, 242, 879, 735))
pixels = list(screen.getdata())

dico_pos = {0: 0, 1: 55, 2: 110, 3: 165, 4: 220, 5: 275, 6: 331, 7: 385, 8: 440}

differentes_coul = set()

for y in range(9):
    for x in range(9):
        x2, y2 = dico_pos[x], dico_pos[y]
        i = (y2 + 3 ) * screen.width + x2 + 3
        differentes_coul.add(pixels[i])
        pixels[i] = 255, 0, 0

print(differentes_coul)
new_img = Image.new(screen.mode, screen.size)
new_img.putdata(pixels)
new_img.save("test.png")
