from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')


@app.route("/SignUp")
def signUp():
    #return render_template('index.html')
    return "Placeholder for sign up page"


@app.route("/SignIn")
def signIn():
    #return render_template('index.html')
    return "Placeholder for sign in page"




if __name__ == "__main__":
	app.run()