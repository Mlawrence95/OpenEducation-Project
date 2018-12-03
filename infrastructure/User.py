class User:

    def __init__(self, email, name, data):
        self.email = email
        self.name = name
        self.data = data.copy()

    ## Wants:
    ## performance history
    ## a name to display


    def recordOutcome(questionID, outcome):
            self.data.loc[questionID] = outcome

    def getAllHistory():
        return self.data

    def getCategoricalHistory(category)
        catData = self.data[self.data['subject'] == category]
        return catData
