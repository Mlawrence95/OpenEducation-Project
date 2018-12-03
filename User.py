import pandas as pd

class User:
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

    def getPerformance(self):

        qid = []
        answered = []
        correct = []

        for k, v in self.recorded.items():
            qid += [k]
            answered += [v]
            correct += [self.data.loc[k, "AnswerKey"]]

        qid = pd.Series(qid)
        answered = pd.Series(answered)
        correct = pd.Series(correct)

        data = {"Question ID": qid,
                "My Answer": answered,
                "correct": correct}

        return pd.DataFrame(data)

    def htmlTable(self):
        return self.getPerformance().to_html()

