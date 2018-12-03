class Profile:

    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    import User
    import Category

    def __init__(self, userid, database):
        self.uid = userid
        self.db = database

        self.user = User.User(self.uid, self.db)
        self.data = self.db.query("SELECT * FROM Questions WHERE Category == category")


    def categoryPerformance(self, category):

