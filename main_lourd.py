from PIL import ImageGrab, Image
import easyocr
from time import time
import numpy as np
debut = time()


# class node:
#     def __init__(self,liste):
#

def screenshot(): ImageGrab.grab((386, 242, 879, 735)).save("capture.png")


# screenshot()

longueur_case = 55

reader = easyocr.Reader(['fr'])
image = Image.open("capture.png")
sudo_liste = []
for y in range(9):
    sudo_liste.append([])
    for x in range(9):
        left = x * longueur_case
        top = y * longueur_case
        right = left + longueur_case
        bottom = top + longueur_case
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image.show()
        nb = reader.readtext(np.array(cropped_image))
        print("___________________________________")
        print(x, y)
        print((left, top), (right, bottom))

        if nb:
            print(nb)
        #     sudo_liste[y].append(nb[1])
        # else:
        #     sudo_liste[y].append(" ")

for ligne in sudo_liste:
    print(ligne)

""" # v1
result = reader.readtext(image, allowlist="0123456789")
nb_a_classer = result[0][0]
espace_entre_case = 500/9
print(espace_entre_case)
droite = nb_a_classer[1][0]
gauche = nb_a_classer[0][0]
bas = nb_a_classer[2][1]
haut = nb_a_classer[1][1]

case = (floor((droite-gauche)/espace_entre_case),floor((bas-haut)/espace_entre_case))
print((droite,gauche),(droite-gauche),espace_entre_case/(droite-gauche))
print((bas,haut),(bas-haut),espace_entre_case/(bas-haut))
print(case,result[0][1])
"""
""" # V2
result = reader.readtext(image, allowlist="0123456789")
for index in range(len(result)):
    nb_a_classer = result[index][0]
    espace_entre_case = 500 / 9
    droite = nb_a_classer[1][0]
    gauche = nb_a_classer[0][0]
    bas = nb_a_classer[2][1]
    haut = nb_a_classer[1][1]

    case = (floor((droite - gauche) / espace_entre_case), floor((bas - haut) / espace_entre_case))
    # print((droite,gauche),(droite-gauche),espace_entre_case/(droite-gauche))
    # print((bas,haut),(bas-haut),espace_entre_case/(bas-haut))
    print(case,result[index][1])
"""

print(f"{time() - debut} s")
