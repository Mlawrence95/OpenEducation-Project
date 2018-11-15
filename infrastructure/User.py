class User:

    def __init__(self, userid, databaseLoc):
        self.__userID = userid
        self.database = databaseLoc
        #self.achievements = achievements

        self.db = self.database.getDB()


    def getUser(self):
        """
        looks for user's information in mySQL database
        :return:
        """
        # TODO
        return self.db.getUser(self.__userID)

    

    def trophies(self):
        ach = []

        for trophy in self.achievements:
            if trophy.isDone():
                ach += [trophy]

        return ach