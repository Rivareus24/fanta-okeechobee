# region IMPORTS
import json

import gspread
import pandas as pd
from gspread import SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

import bonus as bn
import indexes as ix
import labels as lb
import roles as rl
import util


# endregion

# region FUNCTIONS


def get_bonus():
    return \
        + marksDF[lb.golBns] \
        + marksDF[lb.assBns] \
        + marksDF[lb.gs] * -1 \
        + marksDF[lb.am] * -0.5 \
        + marksDF[lb.es] * -2 \
        + marksDF[lb.au] * -2 \
        + marksDF[lb.rp] * +3 \
        + marksDF[lb.rs] * -2 \
        + marksDF[lb.rf] * +3


# endregion

while True:

    try:
        week_number = int(input("Week number: "))

        if 0 < week_number <= 35:
            break
    except:
        print()

with open('data.json', 'r') as dataFile:
    data = json.load(dataFile)

spreadsheets = data['spreadsheets']
ss_marks = spreadsheets['marks']
ss_fanta = spreadsheets['fanta']

MARKS_SPREADSHEET_NAME = ss_marks['name'] + str(week_number)
MARKS_WORKSHEET_NAME = ss_marks['worksheet_name']
FANTA_SPREADSHEET_NAME = ss_fanta['name']
FANTA_WORKSHEET_NAME = ss_fanta['worksheet_name']

floatLabels = lb.get_float_labels()
intLabels = lb.get_int_labels()

# CREDENTIALS

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'stuff.json',
    ["https://spreadsheets.google.com/feeds",
     "https://www.googleapis.com/auth/drive"])

gc = gspread.authorize(credentials)

# WORKSHEET VOTI

try:
    marksWS = gc.open("Voti_Fantacalcio_Stagione_2018-19_Giornata_").worksheet("Fantagazzetta")
except SpreadsheetNotFound:
    input("SpreadsheetNotFound:")

# GET ALL VALUES

labels = lb.get_labels()
x = marksWS.get_all_values()[4:]
marksDF = pd.DataFrame(x, columns=labels)

# STORE TEAMS THA HAS ALREADY PLAYED

codeCol = marksDF[lb.code]
alreadyPlayedTeams = codeCol.loc[marksDF[lb.code].isin(util.italian_teams)]
alreadyPlayedTeams = alreadyPlayedTeams.values.tolist()

# REMOVE USELESS COLUMNS

marksDF.pop(lb.code)
marksDF.pop(lb.gdv)
marksDF.pop(lb.gdp)

# REMOVE USELESS ROWS

roles = rl.get_roles()
marksDF = marksDF.loc[marksDF[lb.role].isin(roles)]
marksDF = marksDF.loc[marksDF[lb.mark] != '6*']

# ARRANGE COLUMNS TYPES

marksDF[floatLabels] = marksDF[floatLabels].astype(float)
marksDF[intLabels] = marksDF[intLabels].astype(int)

# SUM THE TWO KINDS OF ASSISTS

marksDF[lb.ass] += marksDF[lb.asf]  # TODO check
marksDF.pop(lb.asf)

# CALCULATE GOAL BONUS

marksDF[lb.golBns] = 0.0
marksDF.loc[marksDF[lb.gf] > 0, [lb.golBns]] = \
    marksDF[lb.gf] * marksDF[lb.role].apply(bn.get_gol_value) + \
    marksDF[lb.gf].apply(bn.get_gol_bonus)

# CALCULATE ASSIST BONUS

marksDF[lb.assBns] = 0.0
marksDF.loc[marksDF[lb.ass] > 0, [lb.assBns]] = \
    marksDF[lb.ass] * marksDF[lb.role].apply(bn.get_ass_value) + \
    marksDF[lb.ass].apply(bn.get_ass_bonus)

# CALCULATE TOTAL BONUS

marksDF[lb.bonus] = get_bonus()

# SEPARATE DF TO SPEED UP THE SEARCHING PHASE ??

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# WORKSHEET FANTAOKEECHOBEE
fantaWS = gc.open("FantaOkeechobeeY").worksheet("Scores")

# GET ROWS

rows = ix.Rows(week_number)

firstRow = rows.firstRow
lastRow = rows.lastRow

# GET COLUMNS

teams = ix.Cols().teams

playersDF = pd.read_csv('quotazioni_2018_2019.csv', sep=";")
playersDF[lb.team] = playersDF[lb.team].apply(util.upperCase)

for teamIndex, col in enumerate(teams):

    # if index != 0:
    #     continue

    print(f"{util.okeechobee_teams[teamIndex]} filling data...")

    # Dividere i dataset

    bench = fantaWS.range(f"{col.bench}{firstRow}:{util.getColLetter(col.bench, 1)}{lastRow - 6}")

    list_temp = util.unflatten_list(bench, 2)

    benchDF = pd.DataFrame(list_temp, columns=[lb.role, lb.name])
    benchDF.pop(lb.role)

    benchDF = pd.merge(benchDF, playersDF, on=lb.name, how="left")

    starters = fantaWS.range(f"{col.starters}{firstRow}:{util.getColLetter(col.starters, 1)}{lastRow}")

    list_temp = util.unflatten_list(starters, 2)

    startersDF = pd.DataFrame(list_temp, columns=[lb.role, lb.name])
    startersDF.pop(lb.role)

    startersDF = pd.merge(startersDF, playersDF, on=lb.name, how="left")

    marks = fantaWS.range(f"{col.marks}{firstRow}:{col.marks}{lastRow}")

    bonus = fantaWS.range(f"{col.bonus}{firstRow}:{col.bonus}{lastRow}")

    dataDF = marksDF[[lb.name, lb.mark, lb.bonus]]

    startersDF = pd.merge(startersDF, dataDF, on=lb.name, how="left")

    for index, starter in startersDF.iterrows():

        print(f"{starter[lb.role]} ", end='')

        if starter[lb.team] not in alreadyPlayedTeams:
            continue

        # CHECK IF ALREADY CALCULATED, IN CASE SKIP

        if marks[index].value and bonus[index].value:
            continue

        # CHECK IF HE PLAYED

        if util.isNotNan(starter[lb.mark], starter[lb.bonus]):

            try:
                marks[index].value = starter[lb.mark]

                bonus[index].value = starter[lb.bonus]

            except Exception as err:
                print(f"Error: {err}")

    fantaWS.update_cells(marks)
    fantaWS.update_cells(bonus)

    print("\n")
