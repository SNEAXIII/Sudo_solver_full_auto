from pyautogui import locateOnScreen
region = (left, top, longueur_case, longueur_case)
results = locateOnScreen(f"nombres/", region=region)
            #     if results is not None:
            #         sudo_liste[y].append(" ")