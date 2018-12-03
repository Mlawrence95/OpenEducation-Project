import pandas as pd

class User:
    def __init__(self, email, name, data):
        self.email = email
        self.name = name
        self.data = data
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
        outcome = []

        for k, v in self.recorded.items():
            assert type(k) == int
            assert type(v) == str

            qid += [k]
            answered += [v]
            correct += [self.data.loc[k, "AnswerKey"]]
            outcome += [self.data.loc[k, "AnswerKey"].strip().lower() == v.strip().lower()]

        qid = pd.Series(qid)
        answered = pd.Series(answered)
        correct = pd.Series(correct)

        data = {"QuestionID": qid,
                "Response": answered,
                "Correct": correct,
                "Outcome": outcome}

        data = pd.DataFrame(data)
        #data['Outcome'] = data['Response'] == data['Correct']

        return data

    def htmlTable(self):
        return self.getPerformance().to_html()

    def joinOnOriginal(self):

        perf = self.getPerformance()

        keep = list(perf.columns) + ['schoolGrade', 'question', 'subject']
        joined = perf.join(self.data, on='QuestionID')[keep]

        return joined


