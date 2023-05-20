from typing import Optional
from time import time, sleep
from PIL import ImageGrab, Image
from mouse import click, move
from keyboard import press_and_release
from numers_list import numbers_list

debut = time()


class Field:

    def __init__(self, x: int, y: int, i: int, value: Optional[int] = None, is_write: bool = False):
        self.x, self.y, self.i = x, y, i
        self.value = value
        self.filled = True if self.value is not None else False
        self.is_write = is_write
        self.reset_white_list()

    def __str__(self):
        return f"{self.value if self.value is not None else self.white_list}"

    def ban_nb(self, nb: int):
        self.white_list.discard(nb)

    def pos(self):
        return self.x, self.y, self.i

    def reset_white_list(self):
        self.white_list = set(range(1, 10)) if self.value is None else set()


class Sudoku:

    def __init__(self):
        self.def_attributes()
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

    def def_attributes(self):
        self.screen = ImageGrab.grab((386, 242, 879, 735))
        self.blacklist_pixel = ((195, 220, 250), (199, 214, 233), (255, 255, 255), (228, 234, 243), (240, 208, 214))
        self.int_symbol = {"1": "&", "2": "é", "3": "\"", "4": "'", "5": "(", "6": "-", "7": "è", "8": "_", "9": "ç"}
        self.numbers_dicto_filled = {f"{nb}": 0 for nb in range(1, 10)}
        self.numbers_pos = numbers_list
        self.x_base = 12
        self.y_base = 9
        self.y_moins = 33
        self.x_plus = 27
        self.longueur_case = 55
        self.dico_pos = {0: 0, 1: 55, 2: 110, 3: 165, 4: 220, 5: 275, 6: 331, 7: 385, 8: 440}

    def solve(self):
        old_count = 0
        while old_count != len(self):
            old_count = len(self)
            self.completeAll()
            _len = len(self)
            if old_count == _len and not _len == 81:
                print("avant aide :", len(self))
                self.pointing_pairs()
                self.completeAll()
                print("avant aide :", len(self))

    def pointing_pairs(self):

        # On regarde les paires pointantes dans les colones
        for column in self.columns:
            if 3 <= len(column.white_list):
                for nb in column.white_list:
                    result = column.count_number(nb)
                    for i, count in enumerate(result):
                        id = column.x // 3 + i * 3
                        current_box = self.boxs[id]
                        if current_box.count_number(nb) == count == 2:
                            for field in column.list:
                                if not field.i == id and nb in field.white_list:
                                    field.ban_nb(nb)
                                    print(f"J'ai blacklist {nb} a la position {field.pos()} avec la colone")

        # On regarde les paires pointantes dans les lignes
        for row in self.rows:
            if 3 <= len(row.white_list):
                for nb in row.white_list:
                    result = row.count_number(nb)
                    for i, count in enumerate(result):
                        id = row.y // 3 * 3 + i
                        current_box = self.boxs[id]
                        if current_box.count_number(nb) == count == 2:
                            for field in row.list:
                                if not field.i == id and nb in field.white_list:
                                    field.ban_nb(nb)
                                    print(f"J'ai blacklist {nb} a la position {field.pos()} avec la ligne")

    def reset_withlist(self):
        for elem in self.boxs:
            elem.reset_white_list()
        for elem in self.columns:
            elem.reset_white_list()
        for elem in self.rows:
            elem.reset_white_list()

        for row in self.rows:
            for field in row.list:
                if not field.filled:
                    field.reset_white_list()
        self.all_blacklist()

    def select_field(self, x: int, y: int) -> Field:
        return self.rows[y].list[x]

    def fill_empty_field(self):
        mid_field = self.longueur_case // 2
        for row in self.rows:
            for field in row.list:
                if field.is_write:
                    move(386 + mid_field + field.x * self.longueur_case, 242 + mid_field + field.y * self.longueur_case,
                         duration=0.001)
                    click()
                    press_and_release(self.int_symbol[str(field.value)])

    def fill_note(self, listed=[]):
        x1, y = 1116, 271
        if ImageGrab.grab((1141, 237, 1141 + 1, 237 + 1)).getpixel((0, 0)) != (61, 108, 223):
            move(x1, y)
            click()
        mid_field = self.longueur_case // 2
        for row in self.rows:
            for field in row.list:
                if not field.is_write:
                    move(386 + mid_field + field.x * self.longueur_case, 242 + mid_field + field.y * self.longueur_case,
                         duration=0.001)
                    click()
                    for nb in field.white_list:
                        if nb in listed or listed == []:
                            press_and_release(self.int_symbol[str(nb)])
        move(x1, y)
        click()

    def clear_note(self):
        mid_field = self.longueur_case // 2
        for row in self.rows:
            for field in row.list:
                if not field.filled:
                    move(386 + mid_field + field.x * self.longueur_case, 242 + mid_field + field.y * self.longueur_case,
                         duration=0.001)
                    click()
                    press_and_release("suppr")

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
        for index, elem in self.numbers_dicto_filled.items():
            print(f"Il y a {elem} fois le chiffre {index}")

    def show_box(self, nb: int):
        print(self.boxs[nb])

    def completeAll(self):

        # ajouter les cases qui ont qu'une seule valeur possible
        for row in self.rows:
            for field in row.list:
                if len(field.white_list) == 1:
                    value = list(field.white_list)[0]
                    x, y, i = field.pos()
                    self.add_field_all(x, y, i, value, True)

        # éléments à placer
        add_dico = set()

        # placer les cases par déduction dans les boites quand il reste une seule case pour un nombre donné
        for box in self.boxs:
            for value in box.white_list:
                who_possible = set()
                for field in box.dico:
                    if not field.filled:
                        if value in field.white_list:
                            who_possible.add((field, value))
                if len(who_possible) == 1:
                    add_dico.add(list(who_possible)[0])

        # placer les cases par déduction dans les lignes quand il reste une seule case pour un nombre donné

        for box in self.rows:
            for value in box.white_list:
                who_possible = set()
                for field in box.list:
                    if not field.filled:
                        if value in field.white_list:
                            who_possible.add((field, value))
                if len(who_possible) == 1:
                    add_dico.add(list(who_possible)[0])

        # placer les cases par déduction dans les colones quand il reste une seule case pour un nombre donné

        for box in self.columns:
            for value in box.white_list:
                who_possible = set()
                for field in box.list:
                    if not field.filled:
                        if value in field.white_list:
                            who_possible.add((field, value))
                if len(who_possible) == 1:
                    add_dico.add(list(who_possible)[0])

        if len(add_dico) != 0:
            self.add_dico(add_dico)

    def assoc_pairs(self):
        # On récupère toutes les cases pouvant prendre la valeur nb et on les organise dans l'ordre
        numbers_possible = [[] for _ in range(9)]
        for row in self.rows:
            for field in row.list:
                if not field.filled:
                    for nb in field.white_list:
                        numbers_possible[nb - 1].append(field)

        # On applique la méthode des paires associées
        for index, number_list in enumerate(numbers_possible):
            number = index + 1
            x_blacklist = set()
            y_blacklist = set()
            numbers_white_list = set()
            numbers_black_list = set()
            for field in number_list:
                if not field in numbers_black_list:
                    add_to_whitelist = True
                    ban_x, ban_y = field.x, field.y
                    for field2 in number_list:
                        if not field2.x == ban_x and not field2.y == ban_y:
                            y_field = self.select_field(field.x, field2.y)
                            x_field = self.select_field(field2.x, field.y)
                            if not y_field.filled and not x_field.filled:
                                numbers_black_list.update({field, field2, x_field, y_field})
                                x_blacklist.update({field.x, field2.x})
                                y_blacklist.update({field.y, field2.y})
                                add_to_whitelist = False
                                break
                    if add_to_whitelist:
                        numbers_white_list.add(field)
            # On retire des notes ce qui est blacklist

            for field in numbers_white_list:
                if field.x in x_blacklist or field.y in y_blacklist:
                    field.ban_nb(number)

    def add_dico(self, add_dico):

        for field_value in add_dico:
            value = field_value[1]
            x, y, i = field_value[0].pos()
            self.add_field_all(x, y, i, value, True)

    def build(self):

        # self.screen_pixel = self.screen.getdata()
        self.boxs = [Box(i) for i in range(9)]
        self.columns = [Column(x) for x in range(9)]
        self.rows = [Row(y) for y in range(9)]

        for y in range(9):
            for x in range(9):
                region = self.select_region(x, y)
                self.detect_and_add_number(region, x, y)

    def pixel_pos(self, tupled) -> int:
        return tupled[1] * 27 + tupled[0]

    def detect_and_add_number(self, region, x, y):
        a_ajouter = None
        if not self.is_empty_region(region):
            for index_number_list, number_list in enumerate(self.numbers_pos):
                index_max = len(number_list[0]) - number_list[1]
                number_pixel = list(region.getdata())
                valid = True
                for index_pixel, pixel in enumerate(number_list[0]):
                    posi = self.pixel_pos(pixel)
                    a = index_pixel < index_max and number_pixel[posi] in self.blacklist_pixel
                    b = index_pixel >= index_max and number_pixel[posi] not in self.blacklist_pixel
                    if a or b:
                        valid = False
                        break
                if valid:
                    a_ajouter = index_number_list + 1
                    break
        self.add_field_all(x, y, x // 3 + y // 3 * 3, a_ajouter)

    def all_blacklist(self):
        for row in self.rows:
            for field in row.list:
                if field.filled:
                    self.blacklist(field)

    def blacklist(self, field):
        y, x, i, value = field.y, field.x, field.i, field.value
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
        for index in range(2, 10):
            set_couleur.add(region.getpixel((14, index)))
        return len(set_couleur) == 1

    def select_region(self, x: int, y: int):
        x2, y2 = self.dico_pos[x] + self.x_base, self.dico_pos[y] + self.y_base
        x3, y3 = x2 + self.x_plus, y2 + self.y_moins
        return self.screen.crop((x2, y2, x3, y3))

    def add_field_all(self, x: int, y: int, i: int, value: int, blacklist: bool = False):
        if isinstance(value, int):
            self.numbers_dicto_filled[str(value)] += 1

        field = Field(x, y, i, value, blacklist)
        self.add_field_box(field)
        self.add_field_column(field)
        self.add_field_row(field)
        if blacklist:
            self.blacklist(field)

    def add_field_box(self, field):
        selected_box = self.boxs[field.i]
        for old_field in selected_box.dico:
            if old_field.pos() == field.pos():
                selected_box.dico.remove(old_field)
                break

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
        self.reset_white_list()

    def __str__(self):
        str = f"\nBox no°{self.i}\n"
        for field in self.dico:
            str += f"{field.pos()} {field}\n"
        return str

    def remove_white_list(self, nb: int):
        self.white_list.discard(nb)

    def update_field_white_list(self, nb: int):
        for field in self.dico:
            field.ban_nb(nb)

    def reset_white_list(self):
        self.white_list = set(range(1, 10))

    def count_number(self, nb: int):
        if not nb in self.white_list:
            return 0
        count = 0
        for field in self.dico:
            if not field.filled and nb in field.white_list:
                count += 1
        return count


class Column:

    def __init__(self, x: int):
        self.x = x
        self.list = [None] * 9
        self.reset_white_list()

    def __str__(self):
        return f"{self.list}"

    def remove_white_list(self, nb: int):
        self.white_list.discard(nb)

    def update_field_white_list(self, nb: int):
        for field in self.list:
            field.ban_nb(nb)

    def reset_white_list(self):
        self.white_list = set(range(1, 10))

    def count_number(self, nb: int):
        count = [0, 0, 0]
        if not nb in self.white_list:
            return count
        for field in self.list:
            if not field.filled and nb in field.white_list:
                count[field.y // 3] += 1
        return count


class Row:

    def __init__(self, y: int):
        self.y = y
        self.list = [None] * 9
        self.reset_white_list()

    def __str__(self):
        return f"{self.list}"

    def remove_white_list(self, nb: int):
        self.white_list.discard(nb)

    def update_field_white_list(self, nb: int):
        for field in self.list:
            field.ban_nb(nb)

    def reset_white_list(self):
        self.white_list = set(range(1, 10))

    def count_number(self, nb: int):
        count = [0, 0, 0]
        if not nb in self.white_list:
            return count
        for field in self.list:
            if not field.filled and nb in field.white_list:
                count[field.x // 3] += 1
        return count


# récuperation du sudoku et enregistrement sous forme d'objet


sudo = Sudoku()

sudo.clear_note()
debut = time()
sudo.solve()
print(f"{time() - debut} s")


sudo.fill_empty_field()
sudo.fill_note([])

# for box in sudo.boxs:
#     dico = {nb: 0 for nb in box.white_list}
#     for field in box.dico:
#         for value in field.white_list:
#             dico[value] += 1
#     for key, value in dico.items():
#         if value == 2:
#             print(box.i, key)
