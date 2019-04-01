import util

#   C               D       E               F           G       H
#   bench_roles     bench   starters_roles  starters    mark    bonus

firstLetter = 'c'

firstRow = 5
lastRow = 16

vertical_step = 16
horizontal_step = 8


class Indexes:

    def __init__(self, offset, letter=firstLetter):
        current_letter = util.getColLetter(letter, offset)

        self.bench = current_letter

        self.starters = util.getColLetter(current_letter, 2)

        self.marks = util.getColLetter(current_letter, 4)

        self.bonus = util.getColLetter(current_letter, 5)


class Cols:
    teams = []

    def __init__(self):
        offset = 0

        for _ in range(8):
            ixs = Indexes(offset)
            self.teams.append(ixs)
            offset += horizontal_step


class Rows:

    def __init__(self, week_number):
        rowOffset = (week_number - 1) * vertical_step
        self.firstRow = firstRow + rowOffset
        self.lastRow = lastRow + rowOffset
