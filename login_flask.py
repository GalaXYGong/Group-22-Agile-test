# a simple login page using flask for testing the usermod.py
from flask import Flask, render_template, url_for, request, redirect
from user_crud_func import auth, sign_up, select_id, select_all
import sqlite3
app = Flask(__name__)

#Homepage thing
@app.route('/homepage')
def homepage():
    return render_template("HomePage.html")

# page of login when you open the website 127.0.0.1:8888/
@app.route('/')
def home():
    return render_template("login.html")

@app.route('/register')
def register_page():
    return render_template("register.html")

# login route making a post request to the server to check the username and password using the auth function from usermod.py
@app.route('/auth/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # print(username, password)
    result = auth(username, password)
    # print(result)
    if result[0]:
        # if the user is authenticated then redirect to the home page with the username
        return render_template('home.html', username=username)
    # if the user is not authenticated then redirect to the login page
    return redirect(url_for('home'))

# register route making a post request to the server to check the username and password using the sign_up function from usermod.py
@app.route('/auth/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    result = sign_up(username, password)
    if result[0]:
        return redirect(url_for('home'))
    return redirect(url_for('register_page'))

#Read database.db get scores for everyone and send them to scores.html. Essentially a "leaderboard".
@app.route('/scores')
def scores():
    scores = select_all("account", "username, score")
    #Sort scores by descending order based on score[1]
    scores.sort(key=lambda x: x[1], reverse=True)
    return render_template('scores.html', scores=scores)

if __name__ == "__main__":
    app.run(debug=True, port=8888) # 端口8888