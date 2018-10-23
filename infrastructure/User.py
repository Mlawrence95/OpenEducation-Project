class User:

    def __init__(self, userid, databaseLoc, achievements, etc):
        self.__userID = userid
        self.database = databaseLoc
        self.achievements = achievements

        self.db = self.database.getDB()


    def getUser(self):
        """
        looks for user's information in mySQL database
        :return:
        """
        return self.db.getUser(self.__userID)

    


