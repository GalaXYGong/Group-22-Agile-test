# a simple login page using flask for testing the usermod.py
from flask import Flask, render_template, url_for, request, redirect, session, flash,jsonify
from model import Word, get_question_dict,generate_question_list
from user_crud_func import auth, sign_up, select_all, show_secure_question,update,update_score
from usermod import execute, select_all, update, check_secure_question, select_password
from manage import return_all_secure_question
import secrets 
import json
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import base64
app = Flask(__name__)
app.secret_key = "d4413d05138d1fa03489e233df6aca24"

# page of login when you open the website 127.0.0.1:8888/

@app.route('/', methods=['GET'])
def home():
    username = session.get('username')
    return render_template("home.html", username=username)

@app.route('/login', methods=['GET'])
def login_page():
    username = session.get('username')
    return render_template("login.html", username=username)

@app.route('/register', methods=['GET'])
def register_page():
    list_of_secure_questions = return_all_secure_question()
    return render_template("register.html", list_of_secure_questions=list_of_secure_questions)

@app.route('/forgot', methods=['GET'])
def forgot_page():
    return render_template("forgot.html")

@app.route("/forgot", methods=['GET'])
def forgot():
    return render_template("forgot.html")

# login route making a post request to the server to check the username and password using the auth function from usermod.py
@app.route('/auth/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    print(f" Testing Login username: {username}, password: {password}")
    #hash the password
    #password = generate_password_hash(password, method='pbkdf2:sha256')
    hash_object = hashlib.sha256(password.encode())
    password = base64.b64encode(hash_object.digest()).decode('utf-8')
    print(f"Testing Login username: {username}, hashed password: {password}")

    result = auth(username, password)
    
    if result[0]:
        session['username'] = username
        # if the user is authenticated then redirect to the home page with the username
        return redirect(url_for('home'))
    else:
        # if the user is not authenticated then redirect to the login page with a message
        session['fail_count'] = session.get('fail_count', 0) + 1
        # if the user tried 5 times then redirect to the login page with a message
        if 3 <= session.get('fail_count') < 5:
            attempts = session.get('fail_count')
            message = f"You tried {attempts} attempts. You have only {5 - attempts} more attempts."
            flash(message)
            
        if session.get('fail_count') == 5:
            message = "You tried 5 attempts. Please try again later."
            flash(message)
            
        return redirect(url_for('login_page'))

# register route making a post request to the server to check the username and password using the sign_up function from usermod.py
@app.route('/auth/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    secure_question1 = request.form.get('secure_question1')
    secure_question2 = request.form.get('secure_question2')
    answer1 = request.form.get('answer1')
    answer2 = request.form.get('answer2')
    print(f"Testing Register username: {username}, password: {password}")


    # Hash the password
    #hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    #Use unsalted hash
    hash_object = hashlib.sha256(password.encode())
    hashed_password = base64.b64encode(hash_object.digest()).decode('utf-8')
    print(f"Testing Registering user: {username}, Hashed password: {hashed_password}")
    
    
    # Pass the hashed password to the sign_up function
    result = sign_up(username, hashed_password, secure_question1, answer1, secure_question2, answer2)
    
    #result = sign_up(username, password, secure_question1, answer1, secure_question2, answer2)
    if result[0]:
        return redirect(url_for('login_page'))
    else:
        return redirect(url_for('register_page'))

# making a post request to the server to get secure questions
@app.route('/get_secure_questions', methods=['POST'])
def get_secure_questions():
    username = request.form.get('username')
    secure_questions = show_secure_question(username)
    return redirect(url_for('forgot_page'), secure_questions=secure_questions)

# logout route to remove the username from the session
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/ranking', methods=['GET'])
def ranking():
    scores = select_all("account", "username, score")
    #Sort the scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)
    return render_template("scores.html", scores=scores)

# profile route to show the profile of the user
@app.route('/profile', methods=['GET'])
def profile():
    username =session.get('username')
    return render_template("profile.html", username=username)

# update the password of the user in the profile page
@app.route('/profile/update/password', methods=['POST'])
def update_password():
    username = session.get('username')
    password = request.form.get('password')
    new_password = request.form.get('new_password')
    # check if the current password is correct
    
    hash_object = hashlib.sha256(password.encode())
    old_password_hash = base64.b64encode(hash_object.digest()).decode('utf-8')
    print(f"Testing Registering user: {username}, Hashed password: {old_password_hash}")

    hash_object = hashlib.sha256(new_password.encode())
    new_password_hash = base64.b64encode(hash_object.digest()).decode('utf-8')
    print(f"Testing Registering user: {username}, Hashed password: {old_password_hash}")

    current_password_db = select_password(username)
    if old_password_hash == current_password_db:
        update("account", "password", new_password_hash, f"username='{username}'")
        return redirect(url_for('login_page'))
    else:
        return redirect(url_for('profile')) 

@app.route('/question')
def question():
    questions_list_json = generate_question_list(14,5,"QUESTION_BLANK")

    return render_template("question.html", questions_list=questions_list_json)

@app.route('/definition')
def definition():
    questions_list_json = generate_question_list(14,5,"QUESTION_DEFINITION")

    return render_template("question.html", questions_list=questions_list_json)
#Test for test_db_data.html
@app.route('/test_db_data')
def test_db_data():
    username = session.get('username')
    #Get blank questions from database
    question_blank = select_all("QUESTION_BLANK")

    #Get defination questions from database
    question_defination = select_all("QUESTION_DEFINITION")

    # Convert the fetched data into JSON strings
    question_blank_json = json.dumps(question_blank)
    question_definition_json = json.dumps(question_defination)
    
    return render_template("test_db_data.html", question_blank=question_blank_json, question_defination=question_definition_json, username=username)
#Route for bonus card game
@app.route('/bonus2')
def bonus2():
    return render_template("cardju.html")

#Test for test_db_data.html using new method
@app.route('/test_get_question_dict')
def test_get_question_dict():
    question_blank = get_question_dict("QUESTION_BLANK", 1)
    question_defination = get_question_dict("QUESTION_DEFINITION", 1)
    username = session.get('username')

    return render_template("test_get_dict.html", question_blank=question_blank, question_defination=question_defination, username=username)


# get the secure questions for the user, and send it to the resetq page
@app.route("/auth/forgot", methods=['POST'])
def forgot_questions():
    username = request.form.get('username')
    # print(username)
    questions = show_secure_question(username)
    if not questions:
        return redirect(url_for('forgot_questions'))
    # return questions
    else:
        session['username'] = username
        session['questions'] = questions
        return redirect(url_for('answer'))
    
# to the reset password page, receive answers here and send it to the resetp route
@app.route("/forgot/answer", methods=['GET'])
def answer():
    username = session.get('username')
    questions = session.get('questions')
    return render_template("answers.html",username=username, questions=questions)

@app.route("/auth/forgot/answer", methods=['POST'])
def answer_questions():
    username = request.form.get('username')
    questions = show_secure_question(username)
    answer1 = request.form.get('answer1')
    answer2 = request.form.get('answer2')
    answers = [answer1,answer2]
    print(answers)
    # print(list_of_secure_questions)
    if check_secure_question(username, questions, answers):
        change_password_temp = request.form.get('password')
        hash_object = hashlib.sha256(change_password_temp.encode())
        new_password_hash = base64.b64encode(hash_object.digest()).decode('utf-8')
        print(f"Testing Registering user: {username}, Hashed password: {new_password_hash}")

        update("account", "password", new_password_hash, f"username='{username}'")
        return redirect(url_for("home"))
    else:
        session['fail_count'] = session.get('fail_count', 0) + 1
        if 3 <= session.get('fail_count') < 5:
            attempts = session.get('fail_count')
            message = f"You tried {attempts} attempts. You have only {5 - attempts} more attempts."
        if session.get('fail_count') == 5:
            message = "You tried 5 attempts. Please try again later."
        return redirect(url_for('forgot_questions'), message) 
############################################################################################################
# a simple testing route 
# route is /test_question
# click on submit button to update the score
# this is a prototype for the question page, when we done implementing the question page, we will remove this route
# and the test_question.html
############################################################################################################
@app.route('/test_question', methods=['GET'])
def test_question():
    return render_template("test_question.html")
# when we click on submit button after answering all quesions in the question page
@app.route("/question/update_score", methods=['POST'])
def update_score_page():
    username = session.get('username')
    data = request.get_json()
    score = data.get('score')
    correct_questions = data.get('correct_questions')
    incorrect_questions = data.get('incorrect_questions')
    update_score(username,score,correct_questions,incorrect_questions)
    return jsonify({'message': 'Score updated successfully'}), 200


if __name__ == "__main__":
    app.run(debug=True, port=8888) # 端口8888