from LogicSudokuSol import grid_to_txt
import sys
sys.setrecursionlimit(5000)


puzzle = [
    [0, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 5, 6, 0, 0],
    [9, 0, 1, 0, 0, 0, 0, 0, 0],
    [8, 0, 6, 0, 1, 0, 0, 7, 0],
    [3, 0, 0, 0, 0, 0, 0, 6, 2],
    [0, 9, 0, 0, 0, 4, 0, 3, 8],
    [5, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 6, 0, 9, 0]
]


def block_coord(x):
    return 3 * (x // 3)


def find_zeros(p):
    zeros = []
    for i in range(9):
        for j in range(9):
            if p[i][j] == 0:
                zeros.append([i, j])
    return zeros


def sudokuSolve(grid, positions=None, option_tree=None, i=0, recurrances=0):
    recurrances += 1
    if option_tree is None:
        option_tree = []

    # only finds the zero positions at the start, so a position history can be kept
    if positions is None:
        positions = find_zeros(grid)

    # establishes grid coord
    x = positions[i][0]
    y = positions[i][1]

    # creates lists of values in the same row, column and 3x3 block, so invalid values are eliminated
    row = grid[x]
    col = [row_list[y] for row_list in grid]
    block = [grid[a][b] for a in range(block_coord(x), block_coord(x) + 3) for b in
             range(block_coord(y), block_coord(y) + 3)]

    # if true, then backtracking occured
    if len(option_tree) != i:
        options = option_tree.pop(-1)
    else:
        # grabs each value between 1 and 9 as long as they aren't in the same row, column or block
        options = [n for n in range(1, 10) if n not in row
                   and n not in col
                   and n not in block]
    # print(f"{options} at {x, y}")
    # print(f"Option Tree: {option_tree}")

    # if there are no options, then this path is wrong
    if len(options) == 0:
        try:
            # clearing invalid entry from tree
            option_tree[-1].pop(0)

            # clearing invalid entry from grid
            prev_x = positions[i-1][0]
            prev_y = positions[i-1][1]
            grid[prev_x][prev_y] = 0

            # starting new recursion with a lower i, so that a new value is picked
            sudokuSolve(grid, positions, option_tree, i=len(option_tree)-1, recurrances=recurrances)
        except Exception as e:
            print(f"Recurrances: {recurrances}")
            if len(find_zeros(grid)) == 0:
                print(f"It took {i} generations to reach a solution.")
                print("Solution Generated!")
                return option_tree
            else:
                # Error detection
                print(e)
                print("Cannot backtrack!")
                print(f" Pos: {x, y}\n i: {i}\n Option Tree: {option_tree}")
                if i == 0:
                    print("i = 0, so options algorithm must be wrong")

    else:
        option_tree.append(options)
        grid[x][y] = options[0]
        sudokuSolve(grid, positions, option_tree, i=len(option_tree), recurrances=recurrances)


if __name__ == "__main__":
    tree = sudokuSolve(puzzle)

    grid_to_txt(puzzle, "backtrackingSolution.txt")
