from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash
import wikifier as wiki

import pandas as pd
import numpy as np
import questionHelpers as qH
import time
from User import User

mysql = MySQL()
app = Flask(__name__)

cachedAnswers = [] 
lastIndex = 0

# Database information is stored in external json for privacy
# database not necessary in current implementation
keys = 'mySQLkeys.json'
with open(keys) as f:
    serverKeys = json.load(f)

app.config['MYSQL_DATABASE_USER'] = serverKeys['username']
app.config['MYSQL_DATABASE_PASSWORD'] = serverKeys['password']
app.config['MYSQL_DATABASE_DB'] = serverKeys['database']
app.config['MYSQL_DATABASE_HOST'] = serverKeys['host']

mysql.init_app(app)


# Abandon MySQL and read Pandas
split = pd.read_csv('data/split.csv')
split['Q only'] = split['question'].apply(qH.getQuestion)
cleanSplit = split[~split['question'].apply(qH.hasChart)].astype(str).reset_index()


defaultUser = User(email="Oski@berkeley.edu", name="Oski", data=cleanSplit)


###############
# Begin Pages #
###############


"""
Home Page
"""
@app.route("/")
def main(user=None):

    if user == None:
        user = defaultUser

    return render_template('index.html', user=user.name)


"""
Sign up page
Not functional without MySQL
"""
@app.route("/SignUp")
def signUp(user=None):

    if user == None:
        user = defaultUser

    return render_template('signUp.html', user=user.name)


"""
Sign in Page
Not functional without mySQL
"""
@app.route("/SignIn", methods=["GET"])
def signIn(user=None):

    if user == None:
        user = defaultUser

    return render_template('SignIn.html', user=user.name)


"""
Form grabber for new user sign up
Not in use without MySQL
"""
@app.route("/NewUser", methods=['POST', 'GET'])
def NewUser(user=None):

    if user == None:
        user = defaultUser

    try:
        _name = request.form['inputName']
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']


        if _name and _username and _password:
            print(_name)

            serverConnection = mysql.connect()
            cursor = serverConnection.cursor()

            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_username,_hashed_password))

            data = cursor.fetchall()

            if len(data) is 0:
                serverConnection.commit()
                return json.dumps({'message':'Welcome to the community!'})

            else:
                return json.dumps({'error':str(data[0])})

        else:
            return json.dumps({'html':'<span>Please enter the required fields.</span>'})



    except Exception as e:
        return json.dumps({'error':str(e)})


    finally:
        cursor.close() 
        serverConnection.close()



"""
The quiz page
"""
@app.route("/Learn", methods=['GET', "POST"])
def Learn(category=None, user=None):

    if user == None:
        user = defaultUser

    global cachedAnswers
    global lastIndex

    # Handles Answers
    if request.method == "POST":
        
        printed =  "Actual is " + str(cachedAnswers[-1]) +", you got " + str(request.form['submission'])+". "
        rightAnswer = str(cachedAnswers[-1]) == str(request.form['submission']).lower().strip()
        user.recordOutcome(lastIndex, str(request.form['submission']))
        time.sleep(0.25)

        # if rightAnswer:
        #     return printed + " Good job!"

        # return printed

    if category == None:
        Category = "Physics"

    if Category != None:

        qs = cleanSplit[cleanSplit['subject'] == Category]
        availableCount = qs.shape[0]

        myQIndex = np.random.choice(availableCount)
        output = qH.dynamicQuestionOutput(myQIndex, qs)

        while (len(output) < 6) | (user.hasSeen(myQIndex)):
            myQIndex = np.random.choice(availableCount)
            output = qH.dynamicQuestionOutput(myQIndex, qs)

        if len(cachedAnswers) == 0:
            cachedAnswers += [output['Correct'].lower().strip()]

        elif cachedAnswers[-1] == output['Correct'].lower().strip(): 
            pass
        else:
            cachedAnswers += [output['Correct'].lower().strip()]

        lastIndex = myQIndex
        ans = qH.answers(output)

        return render_template('Learn.html', output=output, category=Category, answers=ans, user=user.name, correct=output['Correct'].lower().strip())

    return render_template('index.html')


"""
The dashboard page
"""
@app.route("/Dashboard", methods=['GET','POST'])
def Dashboard(user=None):

    if user == None:
        user= defaultUser

    table = user.htmlTable(head=5)
    df = user.getPerformance()
    

    physics_score = user.subjectAccuracy("Physics")
    biology_score = user.subjectAccuracy("Biology")

    biology_numerator = biology_score[1]
    biology_denominator = biology_score[0]
    biology_accuracy = int(np.round(biology_score[2], 2) * 100)

    physics_numerator = physics_score[1]
    physics_denominator = physics_score[0]
    physics_accuracy = int(np.round(physics_score[2], 2) * 100)

    total_questions = biology_denominator + physics_denominator


    wikifier_results = {}
    wikifier_results["Oski"] = "https://en.wikipedia.org/wiki/Oski_the_Bear"
    wikifier_results["Mitosis"] = "https://en.wikipedia.org/wiki/Mitosis"
    wikifier_results["Gravity"] = "https://en.wikipedia.org/wiki/Gravity"

    return render_template('indexStudent.html', user=user.name, table=table, wikifier_results=wikifier_results, 
        physics_numerator = physics_numerator, physics_denominator = physics_denominator, physics_accuracy = physics_accuracy, 
        biology_accuracy = biology_accuracy, biology_numerator = biology_numerator, biology_denominator = biology_denominator, total_questions=total_questions)



if __name__ == "__main__":
    app.run(debug=True)



# Thank you to Jay Raj, @jay3dec, for help and inspiration

# Miguel at https://blog.miguelgrinberg.com/post/about-me
# had great tutorials on Flask

# the blog at https://radiusofcircle.blogspot.com/2016/03/making-quiz-website-with-python.html
# was immensely useful

# https://pythonspot.com/flask-web-forms/
# helped with forms 
