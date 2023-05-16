from PIL import ImageGrab, Image


def pos(tupled) -> int:
    return tupled[1] * 27 + tupled[0]


x_base = 12
y_base = 9
y_moins = 33
x_plus = 27

screen = ImageGrab.grab((365, 244, 858, 737))
pixels = list(screen.getdata())

dico_pos = {0: 0, 1: 55, 2: 110, 3: 165, 4: 220, 5: 275, 6: 331, 7: 385, 8: 440}

black_list = {(187, 222, 251), (226, 235, 243), (195, 215, 234), (255, 255, 255), (247, 207, 214)}

_1 = (((8, 8), (15, 4), (15, 11), (15, 18), (15, 27)), 0)
_2 = (((6, 9), (13, 4), (20, 9), (19, 15), (12, 23), (7, 29), (14, 29), (20, 29)), 0)
_3 = (((6, 8), (13, 4), (18, 6), (20, 10), (16, 16), (11, 16), (21, 23), (13, 29), (6, 25), (7, 12), (6, 21)), 2)
_4 = (((8, 23), (10, 13), (18, 4), (18, 16), (18, 28), (22, 22)), 0)
_5 = (((19, 4), (8, 5), (7, 10), (6, 17), (14, 14), (21, 21), (17, 29), (6, 25), (6, 21)), 1)
_6 = (((21, 9), (14, 4), (6, 10), (5, 19), (14, 29), (22, 22), (14, 14), (21, 13)), 1)
_7 = (((6, 4), (21, 4), (18, 13), (15, 19), (10, 29)), 0)
_8 = (((7, 9), (14, 4), (21, 9), (14, 16), (22, 22), (14, 29), (6, 22), (8, 18), (8, 13)), 0)
_9 = (((6, 26), (13, 30), (20, 26), (22, 17), (13, 4), (5, 13), (13, 20), (6, 22)), 1)

numbers_list = (_1, _2, _3, _4, _5, _6, _7, _8,_9)

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
