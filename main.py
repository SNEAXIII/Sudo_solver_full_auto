from time import time, sleep
from pyautogui import locateOnScreen, screenshot, locate
from PIL import ImageGrab, Image
import os

debut = time()


def screenshoted(): ImageGrab.grab((386, 242, 879, 735)).save("capture.png")


def is_empty(region):
    set_couleur = set()
    for index in range(7, 20):
        set_couleur.add(region.getpixel((25, index)))
    return len(set_couleur) == 1


screen = ImageGrab.grab((386, 242, 879, 735))

longueur_case = 55
numbers = os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\\nombres")[::-1]
sudo_liste = []
for y in range(9):
    sudo_liste.append([])
    for x in range(9):
        left, top = x * longueur_case, y * longueur_case
        region = screen.crop((left, top, left + longueur_case, top + longueur_case))
        a_ajouter = " "
        if not is_empty(region):
            for nb in numbers:
                est_present = locate(f"nombres/{nb}", region, confidence=0.80, grayscale=True)
                if nb in numbers and est_present is not None:
                    a_ajouter = nb[0]
                    break
        sudo_liste[y].append(a_ajouter)

for ligne in sudo_liste:
    print(len(ligne), ligne)

print(f"{time() - debut} s")
