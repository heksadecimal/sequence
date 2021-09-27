class player:
    def __init__(self):
        self.playerScore = 0
        self.playerCards = []
        self.playerBox = [[0] * 10 for _ in " " * 10]
        self.playerBox[0][0] = self.playerBox[0][-1] = self.playerBox[-1][
            0
        ] = self.playerBox[-1][-1] = 1

    def addCard(self, card):
        self.playerCards += card

    def hasWildCard(self):
        return "JC" in self.playerCards or "JD" in self.playerCards

    def hasRemove(self):
        return "JH" in self.playerCards or "JS" in self.playerCards

    def chosenValid(self, x, y, opponentBox, card):
        if self.playerBox[x][y]:
            return False

        if opponentBox[x][y]:
            return self.hasRemove()
        else:
            return card in self.playerCards
