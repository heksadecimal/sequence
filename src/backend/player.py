class player:
    def __init__(self, name):
        self.playerName = name
        self.playerScore = 0
        self.playerCards = []
        self.playerBox = [[0] * 10 for _ in " " * 10]
        self.playerBox[0][0] = self.playerBox[0][-1] = self.playerBox[-1][
            0
        ] = self.playerBox[-1][-1] = 1

    def addCard(self, card):
        self.playerCards += (card,)

    def hasWildCard(self):
        return "JC" in self.playerCards or "JD" in self.playerCards

    def getWildCard(self):
        return "JC" if "JC" in self.playerCards else "JD"

    def hasRemove(self):
        return "JH" in self.playerCards or "JS" in self.playerCards

    def getRemove(self):
        return "JH" if "JH" in self.playerCards else "JS"

    def hasChosenValid(self, x, y, opponentBox, card):
        if self.playerBox[x][y]:
            print("ALREADY THERE")
            return False

        if opponentBox[x][y]:
            if self.hasRemove():
                print("REM: ", self.getRemove())
                self.playerCards.remove(self.getRemove())
                return 2

            print("OPPO THERE")
            return False

        else:
            if card in self.playerCards:
                self.playerCards.remove(card)
                return 1
            elif self.hasWildCard():
                self.playerCards.remove(self.getWildCard())
                return 1

            print("HEHEH")
            return False
