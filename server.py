from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash

import pandas as pd
import numpy as np
import questionHelpers as qH

mysql = MySQL()
app = Flask(__name__)

cachedAnswers = [] 
defaultUser = "Mike"



# Database information is stored in external json for privacy

keys = 'mySQLkeys.json'
with open(keys) as f:
    serverKeys = json.load(f)

app.config['MYSQL_DATABASE_USER'] = serverKeys['username']
app.config['MYSQL_DATABASE_PASSWORD'] = serverKeys['password']
app.config['MYSQL_DATABASE_DB'] = serverKeys['database']
app.config['MYSQL_DATABASE_HOST'] = serverKeys['host']

mysql.init_app(app)


# Abandon MySQL and read Pandas
# dataCSV = pd.read_csv("data/split.csv")

split = pd.read_csv('data/split.csv')
split['Q only'] = split['question'].apply(qH.getQuestion)
cleanSplit = split[~split['question'].apply(qH.hasChart)].astype(str).reset_index()

# begin pages

@app.route("/")
def main(user=None):

    if user == None:
        user = defaultUser

    return render_template('index.html', user=user)


@app.route("/SignUp")
def signUp(user=None):

    if user == None:
        user = defaultUser

    return render_template('signUp.html', user=user)


@app.route("/SignIn")
def signIn(user=None):

    if user == None:
        user = defaultUser

    return render_template('SignIn.html', user=user)

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



    #return render_template('signUp.html')


@app.route("/Learn", methods=['GET', "POST"])
def Learn(category=None, user=None):

    if user == None:
        user = defaultUser

    global cachedAnswers
    global total 
    global answeredCorrectly

    if request.method == "POST":
        
        printed =  "Actual is " + str(cachedAnswers[-1]) +", you got " + str(request.form['submission'])+". "
        rightAnswer = str(cachedAnswers[-1]).lower().strip() == str(request.form['submission']).lower().strip()

        if rightAnswer:
            return printed + " Good job!"

        return printed



    if category == None:
        Category = "Physics"

    if Category != None:

        qs = cleanSplit[cleanSplit['subject'] == Category]
        availableCount = qs.shape[0]

        myQIndex = np.random.choice(availableCount)
        output = qH.dynamicQuestionOutput(myQIndex, qs)

        while len(output) < 6:
            myQIndex = np.random.choice(availableCount)
            output = qH.dynamicQuestionOutput(myQIndex, qs)

        cachedAnswers += [output['Correct']]



        ans = qH.answers(output)

        return render_template('Learn.html', output=output, category=Category, answers=ans, user=user)

    return render_template('index.html')




@app.route("/Dashboard", methods=['GET'])
def Dashboard(user=None):

    if user == None:
        user = defaultUser

    return render_template('Dashboard.html', user=user)



if __name__ == "__main__":
    app.run(debug=True)



# Thank you to Jay Raj, @jay3dec, for help and inspiration
# Miguel at https://blog.miguelgrinberg.com/post/about-me
# had great tutorials on Flask
# the blog at https://radiusofcircle.blogspot.com/2016/03/making-quiz-website-with-python.html
# was immensely useful
# https://pythonspot.com/flask-web-forms/
# helped with forms 
