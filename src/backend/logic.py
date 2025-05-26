import random
from collections import defaultdict
from PyQt6.QtWidgets import QLabel
from backend.player import player


class Game:
    def __init__(self):
        self.deck = [
            f"{i}{j}"
            for i in list("KQJA") + list(map(str, range(2, 11)))
            for j in "SHCD"
        ] * 2

        self.board = [
            ["XX", "6D", "7D", "8D", "9D", "10D", "QD", "KD", "AD", "XX"],
            ["5D", "3H", "2H", "2S", "3S", "4S", "5S", "6S", "7S", "AC"],
            ["4D", "4H", "KD", "AD", "AC", "KC", "QC", "10C", "8S", "KC"],
            ["3D", "5H", "QD", "QH", "10H", "9H", "8H", "9C", "9S", "QC"],
            ["2D", "6H", "10D", "KH", "3H", "2H", "7H", "8C", "10S", "10C"],
            ["AS", "7H", "9D", "AH", "4H", "5H", "6H", "7C", "QS", "9C"],
            ["KS", "8H", "8D", "2C", "3C", "4C", "5C", "6C", "KS", "8C"],
            ["QS", "9H", "7D", "6D", "5D", "4D", "3D", "2D", "AS", "7C"],
            ["10S", "10H", "QH", "KH", "AH", "2C", "3C", "4C", "5C", "6C"],
            ["XX", "9S", "8S", "7S", "6S", "5S", "4S", "3S", "2S", "XX"],
        ]

        random.shuffle(self.deck)
        self.pos = defaultdict(list)
        self.used = defaultdict(int)
        self.coins = defaultdict(QLabel)
        self.filled = [[0] * 10 for _ in " " * 10]
        self.winner = False

    def storeLocations(self):
        for i in range(10):
            for j in range(10):
                self.pos[self.board[i][j]] += ((i, j),)

    def distribute(self, player: player):
        for _ in range(5):
            player.addCard(self.getNewCard())

    def getNewCard(self):
        while self.deck:
            newCard = self.deck.pop()
            if not self.used[newCard] == 2:
                self.used[newCard] += 1
                return newCard
        return False

    def checkSequence(self, x, y, obj):
        # check up - down

        total = 0
        b = d = y
        while b >= 0:
            if obj.playerBox[x][b]:
                total += 1
            else:
                break
            b -= 1

        while d < 10:
            if obj.playerBox[x][d]:
                total += 1
            else:
                break
            d += 1

        obj.playerScore += total >= 6

        # check left - right

        total = 0
        a = c = x
        while a:
            if obj.playerBox[a][y]:
                total += 1
            else:
                break
            a -= 1

        while c < 10:
            if obj.playerBox[c][y]:
                total += 1
            else:
                break
            c += 1

        obj.playerScore += total >= 6

        # check left - diagonal

        total = 0
        a = c = x
        b = d = y
        while a and b:
            if obj.playerBox[a][b]:
                total += 1
            else:
                break
            a -= 1
            b -= 1

        while c < 10 and d < 10:
            if obj.playerBox[c][d]:
                total += 1
            else:
                break
            c += 1
            d += 1

        obj.playerScore += total >= 6

        # check right - diagonal

        total = 0
        a = c = x
        b = d = y
        while a and b < 9:
            if obj.playerBox[a][b]:
                total += 1
            else:
                break
            a -= 1
            b += 1

        while c < 9 and d:
            if obj.playerBox[c][d] == obj.playerBox[c + 1][d - 1]:
                total += 1
            else:
                break
            c += 1
            d -= 1

        obj.playerScore += total >= 6
        if obj.playerScore > 0:
            self.winner = True

    def setBox(self, player: player, opponent, x, y):
        if self.board[x][y] == "XX":
            return False

        ok = player.hasChosenValid(x, y, opponent, self.board[x][y])
        if ok == 0:
            print("NOT VALID", self.board[x][y], player.playerCards)

        elif ok == 1:
            player.playerBox[x][y] = 1
            self.checkSequence(x, y, player)
            self.filled[x][y] = 1
            return ok

        else:
            self.filled[x][y] = 0
            opponent[x][y] = 0

        return ok

    def makeRandomMove(self, player: player, opponent: player):
        while True:
            card = random.choice(player.playerCards)  # one eye jack
            if card in ("JH", "JS"):
                for i in range(10):
                    for j in range(10):
                        if self.board[i][j] == "XX":
                            continue
                        if opponent.playerBox[i][j]:
                            opponent.playerBox[i][j] = 0
                            player.playerCards.remove(card)
                            self.filled[i][j] = 0
                            player.addCard(self.getNewCard())
                            return (i, j, 0)
                return False

            elif card in ("JD", "JC"):  # two eye jack
                for i in range(10):
                    for j in range(10):
                        if self.board[i][j] == "XX":
                            continue
                        if (
                            player.playerBox[i][j] == 0
                            and opponent.playerBox[i][j] == 0
                        ):
                            player.playerBox[i][j] = 1
                            self.filled[i][j] = 1
                            self.checkSequence(i, j, player)
                            player.playerCards.remove(card)
                            player.addCard(self.getNewCard())
                            return (i, j, 1)
                return False

            else:  # normal card
                for i in range(10):
                    for j in range(10):
                        if self.board[i][j] == "XX":
                            continue
                        if (
                            self.board[i][j] == card
                            and player.playerBox[i][j] == opponent.playerBox[i][j] == 0
                        ):
                            self.filled[i][j] = 1
                            player.playerBox[i][j] = 1
                            self.checkSequence(i, j, player)
                            player.playerCards.remove(card)
                            player.addCard(self.getNewCard())
                            return (i, j, 1)

                player.playerCards.remove(card)
                player.addCard(self.getNewCard())
                return False
