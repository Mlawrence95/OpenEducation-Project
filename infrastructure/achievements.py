class Achievement:

    def __init__(self, category, name, endpoint):
        self.category = category
        self.name = name

        self.score = None
        self.endPoint = endpoint

    def getCategory(self):
        return self.category

    def Score(self):

        if self.score is not None:
            return self.score
        return "You don't have a score yet"

    def Goal(self):
        return self.endPoint

    def incrementScore(self, amount=1):

        if self.score is not None:
            self.score += amount
            return

        self.score = amount

    def isDone(self):
        return self.Score() >= self.Goal()


    def Name(self):
        return self.name

