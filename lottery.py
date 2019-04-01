import json
import random
import time

import gspread
from gspread import SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials


class Team:
    def __init__(self, name, first, other):
        self.name = name
        self.first = first
        self.other = other


teams = [
    Team("BluesBrazzeReus", 0, 5),
    Team("Blaster Master", 1, 12),
    Team("Real Bulls", 0, 9),
    Team("Fottenham", 75, 28),
    Team("Ertha Vernello", 0, 4),
    Team("Rutti di Bosco", 5, 16),
    Team("Atalenta", 19, 21),
    Team("Atletico manontroppo", 0, 7)
]

team_cell = "F6"
pick_number_cell = "C6"

rand = random.SystemRandom()


def setupGDrive():
    with open('data.json', 'r') as dataFile:
        data = json.load(dataFile)

    spreadsheets = data['spreadsheets']
    ss_fanta = spreadsheets['fanta']

    FANTA_SPREADSHEET_NAME = ss_fanta['name']

    scope = [
        data['scope']['feeds'],
        data['scope']['auth']
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        data['json-file'], scope)

    gc = gspread.authorize(credentials)

    try:
        return gc.open(FANTA_SPREADSHEET_NAME).worksheet("Draft Lottery")
    except SpreadsheetNotFound:
        input("SpreadsheetNotFound:")


def getBallsFirstRound():
    balls = []
    for team in teams:
        balls = balls + [team.name] * team.first
    return balls


def getBallsOtherRound():
    balls = []
    for team in teams:
        balls = balls + [team.name] * team.other
    return balls


def updatePercentages(balls, fantaWS):
    percentages = fantaWS.range("C3:J3")

    for idx, percentage in enumerate(percentages):
        occurrences = balls.count(teams[idx].name)
        percentage.value = occurrences / len(balls)

    fantaWS.update_acell(team_cell, "")
    fantaWS.update_cells(percentages)


def setRandomTeam(fantaWS):
    team_selected = rand.choice(balls)

    fantaWS.update_acell(team_cell, team_selected)

    return team_selected


def updateBalls(balls, team_selected):
    return list(filter((team_selected).__ne__, balls))


if __name__ == "__main__":

    fantaWS = setupGDrive()

    balls = getBallsFirstRound()

    for index in range(4):
        time.sleep(1)

        updatePercentages(balls, fantaWS)

        fantaWS.update_acell(pick_number_cell, f"{index + 1}°")

        time.sleep(1)

        team_selected = setRandomTeam(fantaWS)

        balls = updateBalls(balls, team_selected)

    balls = getBallsOtherRound()

    for index in range(8):

        time.sleep(1)

        updatePercentages(balls, fantaWS)

        fantaWS.update_acell(pick_number_cell, f"{index + 5}°")

        time.sleep(1)

        team_selected = setRandomTeam(fantaWS)

        balls = updateBalls(balls, team_selected)

        if ((index + 1) % 8 == 0):
            balls = getBallsOtherRound()
