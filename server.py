from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database information is stored in external json

keys = 'mySQLkeys.json'
with open(keys) as f:
    serverKeys = json.load(f)

app.config['MYSQL_DATABASE_USER'] = serverKeys['username']
app.config['MYSQL_DATABASE_PASSWORD'] = serverKeys['password']
app.config['MYSQL_DATABASE_DB'] = serverKeys['database']
app.config['MYSQL_DATABASE_HOST'] = serverKeys['host']

mysql.init_app(app)



# begin pages

@app.route("/")
def main():
    return render_template('index.html')


@app.route("/SignUp")
def signUp():
    return render_template('signUp.html')


@app.route("/SignIn")
def signIn():
    #return render_template('index.html')
    return "Placeholder for sign in page"

@app.route("/NewUser", methods=['POST'])
def NewUser():

    _name = request.form['inputName']
    _username = request.form['inputUsername']
    _password = request.form['inputPassword']


    if _name and _username and _password:

        serverConnection = mysql.connect()
        cursor = serverConnection.cursor()

        _hashed_password = generate_password_hash(_password)
        cursor.callproc('sp_createUser',(_name,_username,_hashed_password))

        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'Welcome to the community!'})

        else:
            return json.dumps({'error':str(data[0])})

    else:
        return json.dumps({'html':'<span>Please enter the required fields.</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
conn.close()



    #return render_template('signUp.html')



if __name__ == "__main__":
    app.run()