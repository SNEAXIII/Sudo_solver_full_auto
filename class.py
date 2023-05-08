from typing import Optional
from time import time, sleep
from pyautogui import locate
from PIL import ImageGrab, Image
import os
import mouse
import keyboard

debut = time()


class Sudoku:

    def __init__(self, png: Optional[str] = None):
        self.blacklist_pixel = ((195, 220, 250), (199, 214, 233), (228, 234, 243))
        self.numbers_dicto = {f"{nb}": 0 for nb in range(1, 10)}
        self.boxs = [Box(i) for i in range(9)]
        self.columns = [Column(x) for x in range(9)]
        self.rows = [Row(y) for y in range(9)]
        self.longueur_case = 55
        self.numbers = os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}\\nombres")[::-1]
        self.screen = Image.open(png) if png is not None else ImageGrab.grab((386, 242, 879, 735))
        self.build()
        self.all_blacklist()

    def __str__(self):
        str = ""
        for row in self.rows:
            str += "["
            for field in row.list:
                str += f"{field if field.value is not None else ' '}, "
            str = str[:-2] + "]\n"
        return str[:-1]

    def __len__(self):
        count = 0
        for row in self.rows:
            for field in row.list:
                if field.filled:
                    count += 1
        return count

    def select_field(self,x:int,y:int):
        return self.rows[y].list[x]

    def show(self, id: int, type: str):
        if type == "box":
            for index, item in enumerate(self.boxs[id].dico):
                print(index, item)
        if type == "row":
            for index, item in enumerate(self.rows[id].list):
                print(index, item)
        if type == "column":
            for index, item in enumerate(self.columns[id].list):
                print(index, item)

    def show_numbers(self):
        for index, elem in self.numbers_dicto.items():
            print(f"Il y a {elem} fois le chiffre {index}")

    def completeAll(self):

        for row in self.rows:
            for field in row.list:
                if not field.filled and len(field.white_list) == 1:
                    value = list(field.white_list)[0]
                    x, y, i = field.pos()
                    self.add_field_all(x, y, i, value,True)
        a = 0


    def build(self):
        for y in range(9):
            for x in range(9):
                region = self.select_region(x, y)
                a_ajouter = None
                if not self.is_empty_region(region):
                    region = self.remove_background(region.convert('RGBA'))
                    for nb in self.numbers:
                        est_present = locate(f"nombres/{nb}", region, confidence=0.84, grayscale=True)
                        if nb in self.numbers and est_present is not None:
                            a_ajouter = int(nb[0])
                            break
                self.add_field_all(x, y, x // 3 + y // 3 * 3, a_ajouter)

    def remove_background(self, region):
        region_no_bg = []
        for item in region.getdata():
            pixel = (item[0], item[1], item[2])
            if pixel in self.blacklist_pixel:
                region_no_bg.append((255, 255, 255, item[3]))
            else:
                region_no_bg.append(item)
        region.putdata(region_no_bg)
        return region

    def all_blacklist(self):
        for row in self.rows:
            for field in row.list:
                if field.filled:
                    self.blacklist(field)

    def blacklist(self, field):
        value = field.value
        y = field.y
        x = field.x
        i = field.i
        for item in self.rows[y].list:
            if not item.filled:
                self.rows[y].remove_white_list(value)
        for item in self.columns[x].list:
            if not item.filled:
                self.columns[x].remove_white_list(value)
        for item in self.boxs[i].dico:
            if not item.filled:
                self.boxs[i].remove_white_list(value)
        self.rows[y].update_field_white_list(value)
        self.columns[x].update_field_white_list(value)
        self.boxs[i].update_field_white_list(value)

    def is_empty_region(self, region):
        set_couleur = set()
        for index in range(7, 20):
            set_couleur.add(region.getpixel((25, index)))
        return len(set_couleur) == 1

    def select_region(self, x: int, y: int):
        left, top = x * self.longueur_case, y * self.longueur_case
        return self.screen.crop((left, top, left + self.longueur_case, top + self.longueur_case))

    def add_field_all(self, x: int, y: int, i: int, value: int,blacklist:bool = False):
        if isinstance(value, int):
            self.numbers_dicto[str(value)] += 1
        field = Field(x, y, i, value)
        self.add_field_box(field)
        self.add_field_column(field)
        self.add_field_row(field)
        if blacklist:
            self.blacklist(field)

    def add_field_box(self, field):
        selected_box = self.boxs[field.i]
        selected_box.dico.add(field)
        if field.value is not None:
            if field.value in selected_box.white_list:
                selected_box.white_list.discard(field.value)
            else:
                raise ValueError(f"The field {field} already exist the box n°{selected_box.i}")

    def add_field_column(self, field):
        selected_column = self.columns[field.x]
        selected_column.list[field.y] = field
        if field.value is not None:
            if field.value in selected_column.white_list:
                selected_column.white_list.discard(field.value)
            else:
                raise ValueError(f"The field {field} already exist the column n°{selected_column.x}")

    def add_field_row(self, field):
        selected_row = self.rows[field.y]
        selected_row.list[field.x] = field
        if field.value is not None:
            if field.value in selected_row.white_list:
                selected_row.white_list.discard(field.value)
            else:
                raise ValueError(f"The field {field} already exist the row n°{selected_row.y}")


class Box:

    def __init__(self, i: int):
        self.i = i
        self.dico = set()
        self.white_list = set(range(1, 10))

    def __str__(self):
        return f"{self.dico}"

    def remove_white_list(self, nb: int):
        self.white_list.discard(nb)

    def update_field_white_list(self, nb: int):
        for field in self.dico:
            field.ban_nb(nb)


class Column:

    def __init__(self, x: int):
        self.x = x
        self.list = [None] * 9
        self.white_list = set(range(1, 10))

    def __str__(self):
        return f"{self.list}"

    def remove_white_list(self, nb: int):
        self.white_list.discard(nb)

    def update_field_white_list(self, nb: int):
        for field in self.list:
            field.ban_nb(nb)


class Row:

    def __init__(self, y: int):
        self.y = y
        self.list = [None] * 9
        self.white_list = set(range(1, 10))

    def __str__(self):
        return f"{self.list}"

    def remove_white_list(self, nb: int):
        self.white_list.discard(nb)

    def update_field_white_list(self, nb: int):
        for field in self.list:
            field.ban_nb(nb)


class Field:

    def __init__(self, x: int, y: int, i: int, value: Optional[int] = None):
        self.x, self.y, self.i = x, y, i
        self.value = value
        self.filled = True if self.value is not None else False
        self.is_write = True if self.value is not None else False
        self.white_list = set(range(1, 10)) if self.value is None else set()

    def __str__(self):
        return f"{self.value if self.value is not None else self.white_list}"

    def ban_nb(self, nb: int):
        self.white_list.discard(nb)

    def pos(self):
        return self.x, self.y, self.i


sudo = Sudoku()

print(len(sudo))
print(sudo)

print(sudo.select_field(6,2).white_list)
sudo.completeAll()
print(len(sudo))
print(sudo.select_field(6,2).white_list)

a = 0


print(f"{time() - debut} s")
