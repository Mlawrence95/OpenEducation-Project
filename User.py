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
        """
        Returns true if questions has been answered already, 
        else false
        """
        return questionID in self.recorded.keys()

    def recordOutcome(self, questionID, outcome):
        """
        Given index of question and what the student answers

        creates a record of the student's mark

        returns nothing (void)
        """
        self.recorded[questionID] = outcome

    def getAllHistory(self):
        """
        returns dictionary of raw performance results
        """
        return self.recorded

    def getPerformance(self):
        """
        returns dataframe of:

        question id (questionID)
        correct answer (correct)
        student response (response)
        if student was correct  (outcome)
        """

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
        return data

    def htmlTable(self):
        """
        Returns HTML rendering of joined performance table
        """
        return self.joinOnOriginal().to_html()

    def joinOnOriginal(self):
        """
        Joins performance data with starting data

        returns dataframe of performance data as well
        as the subject, school grade, and question
        """

        perf = self.getPerformance()
        keep = list(perf.columns) + ['schoolGrade', 'question', 'subject']
        joined = perf.join(self.data, on='QuestionID')[keep]

        return joined

    def getSubject(self, category):
        """
        category is "Physics" or "Biology"

        returns dataframe of those questions
        that have been answered
        """
        data = self.joinOnOriginal()
        subset = data[data['subject'] == category]
        return subset

    def subjectAccuracy(self, category):
        """
        category is "Physics" or "Biology"

        returns [total answered, total correct, accuracy]
        """

        data = self.getSubject(category)

        count = data.shape[0]
        correct = data['Outcome'].sum()
        accuracy = data['Outcome'].mean()

        return [count, correct, accuracy]

