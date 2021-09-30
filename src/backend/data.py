import json


def getStoredName():
    filename = "userdata.json"
    try:
        with open(filename) as name:
            username = json.load(name)
    except FileNotFoundError:
        return None
    else:
        return username


def getNewName():
    username = input("Enter your name: ")
    filename = "userdata.json"
    with open(filename, "w") as name:
        json.dump(username, name)
    return username


def getGamesPlayed():
    played = 0
    filename = "userdata.json"
    with open(filename, "w") as gamesPlayed:
        json.dump(played, gamesPlayed)
    return played


def getGamesWon():
    won = 0
    filename = "userdata.json"
    with open(filename, "w") as gamesWon:
        json.dump(won, gamesWon)
    return won


def getGamesLost():
    lost = 0
    filename = "userdata.json"
    with open(filename, "w") as gamesLost:
        json.dump(lost, gamesLost)
    return lost


def getNumberOfSequence():
    count = 0
    filename = "userdata.json"
    with open(filename, "w") as sequenceMade:
        json.dump(count, sequenceMade)
    return count


def getWinRatio():
    ratio = 0
    filename = "userdata.json"
    with open(filename, "w") as winRatio:
        json.dump(ratio, winRatio)
    return ratio
