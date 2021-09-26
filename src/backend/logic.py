import random
from collections import defaultdict


class Game:
    def __init__(self):
        self.deck = [
            f"{i}{j}" for i in list("KQJA") + list(range(1, 11)) for j in "SHCD"
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

        self.botScore = 0
        self.playerScore = 0
        self.playerCards = []
        self.botCards = []
        self.playerBox = [[0] * 10 for _ in " " * 10]
        self.BotBox = [[0] * 10 for _ in " " * 10]
        self.fixedBox = defaultdict(int)
        self.playerBox[0][0] = self.playerBox[0][-1] = self.playerBox[-1][
            0
        ] = self.playerBox[-1][-1] = 1
        self.BotBox[0][0] = self.BotBox[0][-1] = self.BotBox[-1][0] = self.BotBox[-1][
            -1
        ] = 1

        self.chance = 1
        self.used = defaultdict(int)
        self.distribute()

    def distribute(self):
        for _ in range(5):
            self.playerCards += self.deck.pop()
        for _ in range(5):
            self.botCards += self.deck.pop()

    def setBox(self, who, x, y):
        current = ["botBox", "playerBox"][who]
        opponent = ["botBox", "playerBox"][1 - who]
        currentCard = ["botCards", "playerCards"][who]

        if eval(f"self.{current}[{x}][{y}] == 1"):
            return False

        if eval(f"self.{opponent}[{x}][{y}] == 1"):
            # if who:
            if eval(f""""JC" in self.{currentCard}"""):
                eval(f"self.{opponent}[{x}][{y}] = 0")
                eval(f"""self.{currentCard}.remove("JC")""")
            elif "JD" in self.playerCards:
                eval(f"self.{opponent}[{x}][{y}] = 0")
                self.playerCards.remove("JD")
            else:
                return False


        else:
            if who:
                if card := self.board[x][y] in self.playerCards:
                    self.playerCards.remove(card)
                else:
                    return False
            else:
                if card := self.board[x][y] in self.botCards:
                    self.botCards.remove(card)
                else:
                    return False

            eval(f"self.{current}[{x}][{y}] = 1")

        self.checkSequence(x, y)
        return True

    def getNewCard(self):
        while self.deck:
            newCard = self.deck.pop()
            if not self.used[newCard] == 2:
                self.used[newCard] += 1
                return newCard

        self.declareWinner()

    def declareWinner(self):
        pass

    def getPlayerCoin(self):
        if self.chance:
            return "./img/coins/blue_coin.png"
        else:
            return "./img/coins/red_coin.png"

    def increaseScore(self, who, count=1):
        eval(f"self.{who} += {count}")

    def checkSequence(self, x, y, who):
        # check left - right
        who = ["botBox", "playerBox"][who]
        score = 0
        sqset = set()
        c = 0
        a = b = y
        z = set()
        while a and eval(f"self.{who}[{x}][{a}] == 1") and c < 6:
            a -= 1
            c += 1
        while b < 10 and eval(f"self.{who}[{x}][{b}] == 1") and c < 6:
            b += 1
            c += 1

        if c == 5:
            for i in range(a, b + 1):
                z.add((x, i))

        sqset.add(frozenset(z))

        c = 0
        a = b = y
        z = set()
        while b < 10 and eval(f"self.{who}[{x}][{b}] == 1") and c < 6:
            b += 1
            c += 1

        while a and eval(f"self.{who}[{x}][{a}] == 1") and c < 6:
            a -= 1
            c += 1

        if c == 5:
            for i in range(a, b + 1):
                z.add((x, i))

        sqset.add(frozenset(z))

        # check up - down
        c = 0
        a = b = x
        z = set()
        while b < 10 and eval(f"self.{who}[{a}][{y}] == 1") and c < 6:
            b += 1
            c += 1

        while a and eval(f"self.{who}[{b}][{y}] == 1") and c < 6:
            a -= 1
            c += 1

        if c == 5:
            for i in range(a, b + 1):
                z.add((i, y))

        sqset.add(frozenset(z))

        c = 0
        a = b = x
        z = set()
        while a and eval(f"self.{who}[{b}][{y}] == 1") and c < 6:
            a -= 1
            c += 1

        while b < 10 and eval(f"self.{who}[{a}][{y}] == 1") and c < 6:
            b += 1
            c += 1

        if c == 5:
            for i in range(a, b + 1):
                z.add((i, y))

        sqset.add(frozenset(z))

        # check left - diagonal
        c = 0
        z = set()

        a, b = x, y
        while a and b and eval(f"self.{who}[{a}][{b}] == 1") and c < 6:
            a -= 1
            b -= 1
            c += 1

        a, b = x, y
        while b < 10 and a < 10 and eval(f"self.{who}[{a}][{b}] == 1") and c < 6:
            b += 1
            a += 1
            c += 1

        if c == 5:
            for i in range(a, b + 1):
                z.add((i, y))

        sqset.add(frozenset(z))

        c = 0
        z = set()

        a, b = x, y
        while b < 10 and a < 10 and eval(f"self.{who}[{a}][{b}] == 1") and c < 6:
            b += 1
            a += 1
            c += 1

        a, b = x, y
        while a and b and eval(f"self.{who}[{a}][{b}] == 1") and c < 6:
            a -= 1
            b -= 1
            c += 1

        if c == 5:
            for i in range(a, b + 1):
                z.add((i, y))

        sqset.add(frozenset(z))

        # check right - diagonal
        c = 0
        z = set()

        a, b = x, y
        while a and b and eval(f"self.{who}[{a}][{b}] == 1") and c < 6:
            a += 1
            b -= 1
            c += 1

        a, b = x, y
        while b < 10 and a < 10 and eval(f"self.{who}[{a}][{b}] == 1") and c < 6:
            b += 1
            a -= 1
            c += 1

        if c == 5:
            for i in range(a, b + 1):
                z.add((i, y))

        sqset.add(frozenset(z))

        c = 0
        z = set()

        a, b = x, y
        while b < 10 and a < 10 and eval(f"self.{who}[{a}][{b}] == 1") and c < 6:
            b += 1
            a -= 1
            c += 1

        a, b = x, y
        while a and b and eval(f"self.{who}[{a}][{b}] == 1") and c < 6:
            a += 1
            b -= 1
            c += 1

        if c == 5:
            for i in range(a, b + 1):
                z.add((i, y))

        sqset.add(frozenset(z))

        self.increaseScore(who, len(sqset))
        for i in sqset:
            for j, k in i:
                self.fixedBox[(j, k)] = 1
