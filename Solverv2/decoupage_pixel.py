from PIL import ImageGrab, Image
from numers_list import numbers_list

def pos(tupled) -> int:
    return tupled[1] * 27 + tupled[0]


x_base = 12
y_base = 9
y_moins = 33
x_plus = 27

screen = ImageGrab.grab((386, 242, 879, 735))
pixels = list(screen.getdata())

dico_pos = {0: 0, 1: 55, 2: 110, 3: 165, 4: 220, 5: 275, 6: 331, 7: 385, 8: 440}

black_list = {(195, 220, 250), (199, 214, 233), (255, 255, 255), (228, 234, 243), (240, 208, 214)}

for y in range(9):
    for x in range(9):
        x2, y2 = dico_pos[x] + x_base, dico_pos[y] + y_base
        x3, y3 = x2 + x_plus, y2 + y_moins
        # for a in range(493):
        #     pixels[y2 * screen.width + a] = 255, 0, 0
        #     pixels[y3 * screen.width + a] = 255, 0, 0
        #     pixels[a * screen.width + x2] = 255, 0, 0
        #     pixels[a * screen.width + x3] = 255, 0, 0
        # i = y2 * screen.width + x2
        # i2 = y3 * screen.width + x3
        # pixels[i] = 255, 0, 0
        # pixels[i2] = 255, 0, 0
        number = screen.crop((x2, y2, x3, y3))
        number.save(f"bulked/{x, y}.png")
        # if y == 0:
        #     number.save(f"test_position/{x}.png")
        for index_number_list, number_list in enumerate(numbers_list):
            index_max = len(number_list[0]) - number_list[1]
            number_pixel = list(number.getdata())
            valid = True
            for index_pixel, pixel in enumerate(number_list[0]):
                posi = pos(pixel)
                a = index_pixel < index_max and number_pixel[posi] in black_list
                b = index_pixel >= index_max and number_pixel[posi] not in black_list
                if a or b:
                    valid = False
                    break
                number_pixel[posi] = 0, 255, 0
            new_number = Image.new(number.mode, number.size)
            new_number.putdata(number_pixel)
            if valid:
                # print(x)
                new_number.save(f"test_position/{index_number_list + 1}/testerpixel{x, y}.png")
            else:
                if number_list == _5:
                    print(x, y)

new_img = Image.new(screen.mode, screen.size)
new_img.putdata(pixels)
# new_img.show()
new_img.save("_grille laser.png")
