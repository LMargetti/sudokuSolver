
class NField:
    def __init__(self, n):
        self.N = n
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.n_places = []
        self.solved = False

    def add_point(self, i, j, cell):
        self.grid[i][j] = cell
        if cell == 1:
            self.n_places += [[i, j]]
            self.calculate_reach(i, j)

    def row(self, i):
        return self.grid[i]

    def col(self, j):
        col_list = []
        for row in self.grid:
            col_list.append(row[j])
        return col_list

    def col_to_grid(self, col, j):
        for i, cell in enumerate(col):
            self.grid[i][j] = col[i]

    def block(self, i, j):
        x = 3 * (i//3)
        y = 3 * (j//3)
        block = []
        for a in range(3):
            for b in range(3):
                block.append(self.grid[x + a][y + b])
        return block

    def blocks(self):
        blocks_list = []
        for m in range(3):
            for n in range(3):
                blocks_list.append(self.block(3*m, 3*n))
        return blocks_list

    def blocks_to_grid(self, blocks):
        rows = []
        for a in range(3):
            for b in range(3):
                row = [blocks[a*3][b], blocks[a*3 + 1][b], blocks[a*3 + 2][b]]
                rows.append(row)
        self.grid = rows

    def calculate_reach(self, i, j):
        # row
        for a in range(9):
            self.grid[i][a] = -1

        # col
        for b in range(9):
            self.grid[b][j] = -1

        # larger block
        x = 3 * (i//3)
        y = 3 * (j//3)
        for c in range(3):
            for d in range(3):
                self.grid[x + c][y + d] = -1

        # maintaining 1 at [i, j]
        self.grid[i][j] = 1

    def single_zero_search(self):
        pnts = []
        # column search
        for j in range(9):
            col = self.col(j)
            if sum(col) == -8:
                i = col.index(0)
                pnts.append([i, j])

        # row search
        for a in range(9):
            row = self.row(a)
            if sum(row) == -8:
                b = row.index(0)
                pnts.append([a, b])

        # block search
        for m in range(3):
            for n in range(3):
                pass

        return pnts

    def check_filled(self):
        rows = [i for [i, _] in self.n_places]
        rows_filled = [n in rows for n in range(9)]
        if all(rows_filled):
            self.solved = True
            return True
        else:
            return False
