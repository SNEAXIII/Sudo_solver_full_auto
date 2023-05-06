from typing import Optional


class Sudoku:

    def __init__(self):
        self.boxs = [Box(i) for i in range(9)]
        self.colums = [Column(x) for x in range(9)]
        self.rows = [Row(y) for y in range(9)]

    def add_field_box(self, field):
        selected_box = self.boxs[(field.x // 3) + (field.y // 3 * 3)]
        selected_box.dico.add(field)
        if field.value is not None:
            if field.value in selected_box.white_list:
                selected_box.white_list.discard(field.value)
            else:
                raise ValueError(f"The field {field} already exist the box n°{selected_box.i}")

    def add_field_column(self, field):
        selected_column = self.colums[field.x]
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

    def add_field_all(self, x: int, y: int, value: int):
        field = Field(x, y, value)
        self.add_field_box(field)
        self.add_field_column(field)
        self.add_field_row(field)


class Box:

    def __init__(self, i: int):
        self.i = i
        self.dico = set()
        self.white_list = set(range(1, 10))

    def __str__(self):
        return f"{self.dico}"


class Column:

    def __init__(self, x: int):
        self.x = x
        self.list = [None] * 9
        self.white_list = set(range(1, 10))

    def __str__(self):
        return f"{self.list}"


class Row:

    def __init__(self, y: int):
        self.y = y
        self.list = [None] * 9
        self.white_list = set(range(1, 10))

    def __str__(self):
        return f"{self.list}"


class Field:

    def __init__(self, x: int, y: int, value: Optional[int] = None):
        self.x, self.y = x, y
        self.value = value
        self.filled = True if self.value is not None else False
        self.is_set = True if self.value is not None else False
        self.white_list = set(range(1, 10)) if self.value is None else set()

    def __str__(self):
        return f"{self.value if self.value is not None else self.white_list}"


sudo = Sudoku()

sudo.add_field_all(0, 0, 1)
sudo.add_field_all(1, 0, 2)

print(sudo.rows[0])
a = 0
a = 0
