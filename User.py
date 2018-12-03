class User:
    import pandas as pandas
    def __init__(self, email, name, data):
        self.email = email
        self.name = name
        self.data = data.copy()
        self.recorded = dict()

    ## Wants:
    ## performance history
    ## a name to display

    def hasSeen(self, questionID):
        return questionID in self.recorded.keys()

    def recordOutcome(self, questionID, outcome):
        self.recorded[questionID] = outcome

    def getAllHistory(self):
        return self.recorded

    def getCategoricalHistory(self, category):
        catData = self.data[self.data['subject'] == category]
        return catData
