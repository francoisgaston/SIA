class Point:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.row == other.row and self.col == other.col
        return False

    def __str__(self):
        return "(" + self.row + "; " + self.col + ")"

    def move(self, delta_row, delta_col):
        return Point(self.row + delta_row, self.col + delta_col)
