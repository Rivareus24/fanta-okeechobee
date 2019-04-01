code, role, name, mark, team = "cod", "role", "name", "mark", "team"

gf, gs = "gf", "gs"

rp, rs, rf = "rp", "rs", "rf"

au = "au"

am, es = "am", "es"

ass, asf = "as", "asf"

gdv, gdp = "gdv", "gdp"

bonus, golBns, assBns = "bonus", "golBns", "assBns"


def get_labels():
    return [
        code, role, name, mark,
        gf, gs,
        rp, rs, rf,
        au,
        am, es,
        ass, asf, gdv, gdp
    ]


def get_int_labels():
    return [
        gf, gs,
        rp, rs, rf,
        au,
        am, es,
        ass, asf
    ]


def get_float_labels():
    return [mark]


def get_main_labels():
    return [name, mark, bonus]
