import random
import string
from collections import defaultdict
import backend.player


class Game:
    def __init__(self):
        self.deck = [
            f"{i}{j}"
            for i in list("KQJA") + list(map(str, range(1, 11)))
            for j in "SHCD"
        ] * 2

        self.board = [
            ["XX", "6D", "7D", "8D", "9D", "10D", "QD", "KD", "AD", "XX"],
            ["5D", "3H", "2H", "2S", "3S", "4S", "5S", "6S", "7S", "AC"],
            ["4D", "4H", "KD", "AD", "AC", "KC", "QC", "10C", "8S", "KC"],
            ["3D", "5H", "QD", "QH", "10H", "9H", "8H", "9C", "9S", "QC"],
            ["2D", "6H", "10D", "KH", "3H", "2H", "7H", "8C", "10S", "10C"],
            ["AS", "7H", "9D", "AH", "4H", "5H", "6H", "7C", "QS", "9C"],
            ["KS", "8H", "8D", "2C", "3C", "4C", "QD", "6C", "KS", "8C"],
            ["QS", "9H", "7D", "6D", "6D", "4D", "QD", "2D", "AS", "7C"],
            ["10S", "10H", "QH", "KH", "AH", "2C", "3C", "4C", "5C", "6C"],
            ["XX", "9S", "8S", "7S", "6S", "5S", "4S", "3S", "2S", "XX"],
        ]

        random.shuffle(self.deck)
        self.used = defaultdict(int)

    def setBox(self, player, opponent, x, y):
        if self.board[x][y] == "XX":
            return False

        if player.hasChosenValid(x, y, opponent, self.board[x][y]):
            player.playerBox[x][y] = 1
            self.checkSequence(x, y, player)
            return True

        return False

    def getNewCard(self):
        while self.deck:
            newCard = self.deck.pop()
            if not self.used[newCard] == 2:
                self.used[newCard] += 1
                return newCard
        return False

    def declareWinner(self):
        pass

    def checkSequence(self, x, y, obj):
        # check up - down
        c = 1
        if x > 1 and x < 10:
            for i in range(1, 10):
                if obj.playerBox[x][i] == obj.playerBox[x][i - 1]:
                    c += 1
                else:
                    c = 1
                if c == 5:
                    obj.playerScore = 1
                    break
        else:
            for i in range(2, 9):
                if obj.playerBox[x][i] == obj.playerBox[x][i - 1]:
                    c += 1
                else:
                    c = 1
                if c == 4 and i == 5 or c == 4 and i == 9:
                    obj.playerScore = 1
                elif c == 5:
                    obj.playerScore = 1

        # check left - right

        c = 1
        if y > 1 and y < 10:
            for i in range(1, 10):
                if obj.playerBox[i][y] == obj.playerBox[i - 1][y]:
                    c += 1
                else:
                    c = 1
                if c == 5:
                    obj.playerScore = 1
                    break
        else:
            for i in range(2, 10):
                if obj.playerBox[i][y] == obj.playerBox[i - 1][y]:
                    c += 1
                else:
                    c = 1
                if c == 4 and i == 5 or c == 4 and i == 9:
                    obj.playerScore = 1
                elif c == 5:
                    obj.playerScore = 1

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

        while c < 10 and b < 10:
            if obj.playerBox[c][d]:
                total += 1
            else:
                break
            c += 1
            d += 1

        obj.playerScore += total >= 4

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

        obj.playerScore += total >= 4
