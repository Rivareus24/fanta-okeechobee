# region IMPORTS

from pprint import pprint

import gspread
import numpy as np
import pandas as pd
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

import bonus as bn
import labels as lb
import roles as rl
import util
import quickstart

# endregion

first_row = 5
last_row = 16

vertical_step = 16
horizontal_step = 8

range_heigth = 12
range_width = 5

fanta_SS_id = quickstart.SAMPLE_SPREADSHEET_ID

range_labels = ["BenRole", "Ben", "StaRole", "Sta", "Mark", "Bonus"]


class Team:

    def __init__(self, name, firstCol, lastCol):
        self.name = name
        self.firstCol = firstCol
        self.lastCol = lastCol


okeechobee_teams = (
    Team("Blues BrazzeReus", "C", "I"),
    Team("Blaster Master", "K", "Q"),
    Team("Real Bulls", "S", "Y"),
    Team("Fottenham", "AA", "AG"),
    Team("Ertha Vernello", "AI", "AO"),
    Team("Rutti Di Bosco FC", "AQ", "AW"),
    Team("Atalenta", "AY", "BE"),
    Team("Atletico manontroppo", "BG", "BM"))


def readWeekNumber():
    while True:

        try:
            week_number = int(input("Week number: "))

            if 0 < week_number <= 35:
                return week_number

            print("Il numero deve essere tra 1 e 35")

        except ValueError:
            print("Il valore deve essere un numero\n")


def getTotalBonus(fanta_marks_DF):
    return \
        + fanta_marks_DF[lb.golBns] \
        + fanta_marks_DF[lb.assBns] \
        + fanta_marks_DF[lb.gs] * -1 \
        + fanta_marks_DF[lb.am] * -0.5 \
        + fanta_marks_DF[lb.es] * -2 \
        + fanta_marks_DF[lb.au] * -2 \
        + fanta_marks_DF[lb.rp] * +3 \
        + fanta_marks_DF[lb.rs] * -2 \
        + fanta_marks_DF[lb.rf] * +3


def getPlayersRolesTeams():
    # ----------------------
    # | role | name | team |
    # ----------------------

    players_DF = pd.read_csv('quotazioni.csv', sep=";")
    players_DF[lb.team] = players_DF[lb.team].apply(util.upperCase)
    return players_DF


def getCredentials():
    return ServiceAccountCredentials.from_json_keyfile_name(
        'stuff.json',
        ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"])


def getServiceV4():
    return discovery.build('sheets', 'v4', credentials=getCredentials())


def getValues(
        spreadsheet_id,
        range_,
        major_dimension='DIMENSION_UNSPECIFIED',
        value_render_option='FORMATTED_VALUE',
        date_time_render_option='SERIAL_NUMBER'):
    request = getServiceV4().spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_,
        majorDimension=major_dimension,
        valueRenderOption=value_render_option,
        dateTimeRenderOption=date_time_render_option)

    return request.execute()


def getCleanMarksDF(week_number):
    marks_WS = gspread.authorize(getCredentials()).open(
        f"Voti_Fantacalcio_Stagione_2018-19_Giornata_{week_number}").worksheet("Fantagazzetta")

    # GET ALL VALUES

    labels = lb.get_labels()
    x = marks_WS.get_all_values()[4:]
    marks_DF = pd.DataFrame(x, columns=labels)

    # STORE TEAMS THA HAS ALREADY PLAYED

    codeCol = marks_DF[lb.code]
    alreadyPlayedTeams = codeCol.loc[marks_DF[lb.code].isin(
        util.italian_teams)]
    alreadyPlayedTeams = alreadyPlayedTeams.values.tolist()

    # REMOVE USELESS COLUMNS

    marks_DF.pop(lb.code)
    marks_DF.pop(lb.gdv)
    marks_DF.pop(lb.gdp)

    # REMOVE USELESS ROWS

    roles = rl.get_roles()
    marks_DF = marks_DF.loc[marks_DF[lb.role].isin(roles)]
    marks_DF = marks_DF.loc[marks_DF[lb.mark] != '6*']

    # ARRANGE COLUMNS TYPES

    floatLabels = lb.get_float_labels()
    intLabels = lb.get_int_labels()

    marks_DF[floatLabels] = marks_DF[floatLabels].astype(float)
    marks_DF[intLabels] = marks_DF[intLabels].astype(int)

    # SUM THE TWO KINDS OF ASSISTS

    marks_DF[lb.ass] += marks_DF[lb.asf]  # TODO check
    marks_DF.pop(lb.asf)

    # CALCULATE GOAL BONUS

    marks_DF[lb.golBns] = 0.0
    marks_DF.loc[marks_DF[lb.gf] > 0, [lb.golBns]] = \
        marks_DF[lb.gf] * marks_DF[lb.role].apply(bn.get_gol_value) + \
        marks_DF[lb.gf].apply(bn.get_gol_bonus)

    # CALCULATE ASSIST BONUS

    marks_DF[lb.assBns] = 0.0
    marks_DF.loc[marks_DF[lb.ass] > 0, [lb.assBns]] = \
        marks_DF[lb.ass] * marks_DF[lb.role].apply(bn.get_ass_value) + \
        marks_DF[lb.ass].apply(bn.get_ass_bonus)

    # CALCULATE TOTAL BONUS

    marks_DF[lb.bonus] = getTotalBonus(marks_DF)

    return marks_DF


if __name__ == "__main__":

    # Week number from FantaOkeechobeeY

    week_number = 22  # readWeekNumber()

    # Fantagazzettavoti giornata corrente

    # -------------------------------------
    # | team | role | name | mark | bonus |
    # -------------------------------------

    marks_DF = getCleanMarksDF(week_number)

    # Ciclo Teams

    for index, team in enumerate(okeechobee_teams):
        print(f"{team.name} filling data...\n")

        # RANGE

        response = getValues(
            spreadsheet_id=fanta_SS_id,
            range_='Stand!A1:F7',
            major_dimension='COLUMNS')

    # https://towardsdatascience.com/how-to-access-google-sheet-data-using-the-python-api-and-convert-to-pandas-dataframe-5ec020564f0e

    pprint(response)

    input()

    fanta_marks_DF = getFantaMarksDF()

    players_roles_teams = getPlayersRolesTeams()

    for index, team in enumerate(okeechobee_teams):
        print(f"{team.name} filling data...\n")

        team_range = getRange()

        x = np.reshape(team_range, (13, 6))

        range_DF = pd.DataFrame(x, columns=range_labels)

        y = range_DF

        scores_WS.update_cells(team_range)

        print()

    print("\n\nTHE END")
