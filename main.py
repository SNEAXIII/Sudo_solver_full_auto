from time import time,sleep
from pyautogui import locateOnScreen,screenshot
import os
debut = time()

# screen = (386, 242, 879, 735)

x_base = 386
y_base = 242
longueur_case = 55
files = os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\\nombres")[::-1]
sudo_liste = []
for y in range(9):
    sudo_liste.append([])
    for x in range(9):
        left = x_base + x * longueur_case
        top = y_base + y * longueur_case
        region = (left, top, longueur_case, longueur_case)
        print("___________________________________")
        print(x, y, region)
        # screenshot(region=region).show()
        a_ajouter = " "
        for nb_fichier in files:
            if nb_fichier in files[3:]:
                results = locateOnScreen(f"nombres/{nb_fichier}", confidence=0.80, grayscale=True, region=region)
                if results is not None:
                    a_ajouter = nb_fichier[0]
                    print(a_ajouter)
                    break
        sudo_liste[y].append(a_ajouter)
            # elif nb_fichier in files[:3]:
            #     results = locateOnScreen(f"nombres/{nb_fichier}", region=region)
            #     if results is not None:
            #         sudo_liste[y].append(" ")
            #         break

for ligne in sudo_liste:
    print(len(ligne),ligne)

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
