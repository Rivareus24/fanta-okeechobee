import math


def getIndexZeroBased(letter):
    return ord(letter) - 96


def getLetter(index):
    return chr(index + 96)


def getSum(letter, offset):
    sum = 0

    if len(letter) == 2:
        sum += getIndexZeroBased(letter[0]) * 26
        letter = letter[:-1]

    return sum + getIndexZeroBased(letter) + offset


def getColLetter(letter, offset=0):
    sum = getSum(letter, offset)

    if sum <= 26:
        return getLetter(sum)
    else:
        first_letter = getColLetter(getLetter(round(sum / 26)))
        second_letter = getColLetter(getLetter(sum % 26))
        return f"{first_letter}{second_letter}"


def upperCase(word):
    return word.upper()


italian_teams = (
    "ATALANTA",
    "BOLOGNA",
    "CAGLIARI",
    "CHIEVO",
    "EMPOLI",
    "FIORENTINA",
    "FROSINONE",
    "GENOA",
    "INTER",
    "JUVENTUS",
    "LAZIO",
    "MILAN",
    "NAPOLI",
    "PARMA",
    "ROMA",
    "SAMPDORIA",
    "SASSUOLO",
    "SPAL",
    "TORINO",
    "UDINESE"
)

okeechobee_teams = (
    "Blues BrazzeReus",
    "Blaster Master",
    "Real Bulls",
    "Fottenham",
    "Ertha Vernello",
    "Rutti Di Bosco FC",
    "Atalenta",
    "Atletico manontroppo"
)

bench_height = 6
starters_height = 8


def unflatten_list(list, elementDim):
    if len(list) % elementDim != 0:
        return  # ERROR
    unflattenList = []

    for index in range(0, len(list), elementDim):
        temp_list = []
        for i in range(elementDim):
            temp_list.append(list[index + i].value)
        unflattenList.append(temp_list)

    return unflattenList


def isNotNan(*values):
    values = list(values)
    try:
        for x in values:
            if math.isnan(x):
                return False
        return True
    except:
        return True
