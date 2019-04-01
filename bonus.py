import roles as rl


def get_gol_bonus(goals):
    if goals == 0:      return 0
    if goals == 1:      return 0
    if goals == 2:      return 0.5
    if goals == 3:      return 1 + get_gol_bonus(goals - 1)
    if goals >= 4:      return 2 + get_gol_bonus(goals - 1)


def somma(goals):
    if goals == 0:      return 0
    if goals == 1:      return 0
    if goals >= 1:      return goals + get_gol_bonus(goals - 1)


def get_gol_value(role):
    if role == rl.P:     return 30
    if role == rl.D:     return 4
    if role == rl.C:     return 3.5
    if role == rl.A:     return 3


def get_ass_bonus(assist):
    if assist == 0:     return 0
    if assist == 1:     return 0
    if assist == 2:     return 0.5 + get_ass_bonus(assist - 1)
    if assist > 2:      return 1 + get_ass_bonus(assist - 1)


def get_ass_value(role):
    if role == rl.P:     return 2
    if role == rl.D:     return 1
    if role == rl.C:     return 1
    if role == rl.A:     return 1
