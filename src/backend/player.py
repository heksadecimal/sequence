class player:
    def __init__(self):
        self.playerScore = 0
        self.playerCards = []
        self.playerBox = [[0]*10 for _ in " " * 10]
        self.playerBox[0][0] = self.playerBox[0][-1] = self.playerBox[-1][0] = self.playerBox[-1][-1] = 1

    def addCard(self):
        self.playerCards += self.deck.pop()    