from NField import NField


puzzle = [
    [6, 8, 5, 2, 4, 7, 9, 1, 3],
    [0, 2, 3, 0, 0, 5, 6, 0, 0],
    [9, 0, 1, 8, 0, 0, 0, 0, 0],
    [8, 0, 6, 3, 1, 0, 0, 7, 0],
    [3, 0, 0, 9, 0, 0, 0, 6, 2],
    [0, 9, 0, 0, 0, 4, 0, 3, 8],
    [5, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0],
    [7, 0, 4, 0, 0, 6, 0, 9, 0]
]


def create_fields(p):
    sol = p[:]
    fields = [sol]

    for n in range(1, 10):
        f = NField(n)
        fields.append(f)

    return fields


def init_fields(fields):
    p = fields[0]
    # iterating over each cell
    for i in range(9):
        for j in range(9):
            # skips if cell is empty
            if p[i][j] != 0:
                # iterating over fields
                for n, n_fld in enumerate(fields[1:]):
                    others = [f for f in fields[1:] if f != n_fld]      # all other fields
                    if p[i][j] == n+1:
                        n_fld.add_point(i, j, 1)
                        for fld in others:
                            fld.add_point(i, j, -1)


def solve(fields):
    p = fields[0]
    solved = [False for _ in range(9)]
    loops = 0
    while not all(solved):
        for n_fld in fields[1:]:
            others = [f for f in fields[1:] if f != n_fld]
            pnts = n_fld.single_zero_search()
            for [i, j] in pnts:
                n_fld.add_point(i, j, 1)
                p[i][j] = n_fld.N
                for fld in others:
                    fld.add_point(i, j, -1)
            solved[n_fld.N - 1] = n_fld.check_filled()
        loops += 1
        if loops == 1000:
            print("Solution took too long (Reached the maximum number of loops)")
            print("Sudoku probably cannot be solved without guessing.")
            break

    if all(solved):
        print("Solution generated!")
        print(f"It took {loops} loops to solve this puzzle.")
    return loops


def grid_to_txt(puzzle, filename):
    cell_translate = {
        -1: " - ",
        0: "   ",
        1: " 1 ",
        2: " 2 ",
        3: " 3 ",
        4: " 4 ",
        5: " 5 ",
        6: " 6 ",
        7: " 7 ",
        8: " 8 ",
        9: " 9 "
    }
    row_strings = []

    for i, row in enumerate(puzzle):
        cell_strings = []
        for cell in row:
            cell_strings.append(cell_translate[cell])
        row_strings.append('|'.join(cell_strings))

    field_string = '\n'.join(row_strings)

    with open(filename, "w") as f:
        f.write(field_string)


def main(p):
    grid_to_txt(p, "original_sudoku.txt")
    nfields = create_fields(p)
    init_fields(nfields)
    solve(nfields)

    grid_to_txt(nfields[0], "sudoku_sol.txt")


if __name__ == "__main__":
    main(puzzle)
