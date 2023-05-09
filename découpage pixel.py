from PIL import ImageGrab, Image

x_base = 12
y_base = 9
y_moins = 33
x_plus = 27

screen = ImageGrab.grab((386, 242, 879, 735))
pixels = list(screen.getdata())

dico_pos = {0: 0, 1: 55, 2: 110, 3: 165, 4: 220, 5: 275, 6: 331, 7: 385, 8: 440}

print(screen.size)

for y in range(9):
    for x in range(9):
        x2, y2 = dico_pos[x] + x_base, dico_pos[y] + y_base
        x3, y3 = x2 + x_plus, y2 + y_moins
        for a in range(493):
            pixels[y2 * screen.width + a] = 255, 0, 0
            pixels[y3 * screen.width + a] = 255, 0, 0
            pixels[a * screen.width + x2] = 255, 0, 0
            pixels[a * screen.width + x3] = 255, 0, 0
        i = y2 * screen.width + x2
        i2 = y3 * screen.width + x3
        pixels[i] = 255, 0, 0
        pixels[i2] = 255, 0, 0

new_img = Image.new(screen.mode, screen.size)
new_img.putdata(pixels)
new_img.show()
new_img.save("test.png")
