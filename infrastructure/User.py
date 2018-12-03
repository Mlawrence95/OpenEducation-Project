class User:

    def __init__(self, email, name, data):
        self.email = email
        self.name = name
        self.data = data.copy()
        self.recorded = dict()

    ## Wants:
    ## performance history
    ## a name to display

    def hasSeen(questionID):
        return questionID in self.recorded.keys()

    def recordOutcome(questionID, outcome):
        self.recorded[questionID] = outcome

    def getAllHistory():
        return self.recorded

    def getCategoricalHistory(category):
        catData = self.data[self.data['subject'] == category]
        return catData
