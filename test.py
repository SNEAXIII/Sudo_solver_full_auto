for i in range(9):
    min_row, max_row = i // 3 * 3, i // 3 * 3 + 2
    print(f"box {i} min {min_row} max {max_row}")
print("__________________")
for i in range(9):
    min_col, max_row =  i // 3, i//3+3
    print(f"box {i} min {min_col} max {max_row}")