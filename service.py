import roles


class Player:

    def __init__(self, name, role, mark_avg):
        self.name = name
        self.role = role
        self.mark_avg = mark_avg


class Team:
    p = []
    d = []
    c = []
    a = []
    moneyLeft = 1000

    def __init__(self, name):
        self.name = name


def getTeams():
    return [
        Team('BR'),
        Team('BM'),
        Team('RB'),
        Team('FT'),
        Team('EV'),
        Team('RT'),
        Team('AT'),
        Team('AM')]


def getPlayers():
    return [
        Player('Ibra', roles.A, 10),
        Player('Icardi', roles.A, 7.5),
        Player('Immobile', roles.A, 8.5),
        Player('Pogba', roles.C, 7.2),
        Player('Figo', roles.C, 6.8),
        Player('Zanetti', roles.D, 6.1),
        Player('Nesta', roles.D, 5.8),
        Player('Reina', roles.P, 5.5),
        Player('Dida', roles.P, 6.5)]
