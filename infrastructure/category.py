class Category:

    import pandas as pd
    import numpy as np

    def __init__(self, name, databaseLoc, inactiveIndices=None):
        self.inactive = inactiveIndices
        self.name = name
        self.database = databaseLoc

        # TODO
        self.questionIDs = self.database.indices()

        self.active = []

        if self.inactive is not None:

            for index in self.questionIDs:

                if index not in self.inactive:
                    self.active += [index]


    def removeEntry(self, entry):

        if entry in self.active:

            self.active.remove(entry)
            return 1

        return -1

    def getQuestion(self, entry, random=False):

        question = "placeholder"
        index = 0

        if random:

            index = np.random.sample(self.active, 1)
            question = self.database[index]

        elif entry in self.active:

            index = entry
            question = self.database[entry]

        self.removeEntry(index)

        return question