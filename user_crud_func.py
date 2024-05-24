from usermod import execute, drop, select, update, create, select_username, select_id,select_all, delete,insert,insert_secure_question, show_secure_question,check_secure_question 
from werkzeug.security import check_password_hash
import sqlite3
database = './database/database.db'
# connect to the database
connection = sqlite3.connect(database,check_same_thread=False) # create the file if it does not exist 
cursor = connection.cursor() # cursor is used to interact with the database 
print("Connected to database")

# execute(statement)
############################################################################################################
# execute a statement and commit in the database                                                           #
# the function in the usermod.py file is execute(statement) -> None:                                       #
# need to "from usermod import execute" before calling the function                                        #
# take 1 argument: statement                                                                               #
# e.g. statement= "SELECT * FROM account"                                                                  #
############################################################################################################

# drop(table_name)
############################################################################################################
# drop a table in the database                                                                             #
# the function in the usermod.py file is drop(table_name) -> None:                                         #
# need to "from usermod import drop" before calling the function                                           #
# take 1 argument: table_name                                                                              #
# e.g. drop("account")                                                                                     #
############################################################################################################

# select(）
############################################################################################################
# select all the rows in the table                                                                         #
# the function in the usermod.py file is select(table_name, column_name="*") -> tuple:                     #
# need to "from usermod import select" before calling the function                                         #
# take 2 arguments: table_name, column_name                                                                #
# e.g. select("account", "username, score")                                                                #
# the called function above equals to the following SQL statement                                          #
# SELECT username, score FROM account                                                                      #
# the function returns a tuple of the rows selected                                                        #
# e.g. [('admin', 0), ('ahmed', 100)]                                                                      #
# e.g select("account") # column_name is optional                                                          #
# the called function above equals to the following SQL statement                                          #
# SELECT * FROM account                                                                                    #
# the function returns a tuple of the rows selected                                                        #
# e.g. [(1, 'admin', 'admin123', 'admin', 0), (2, 'ahmed', 'ahmed123', 'user', 100)]                       #
############################################################################################################

# create()
############################################################################################
# adding one new user to the database                                                 #
# arguments for create() is table_name, column_name, value                                 #                 
# ACCOUNT table has columns: id, username, password, role, score                           #  
# eg, create("account", "username,password,role,score", "'ahmed','ahmed123','user',0")     #
# the called function above equals to the following SQL statement                          #
# "INSERT INTO ACCOUNT(username,password,role,score) VALUES ('ahmed','ahmed123','user',0)" #
# please note that the value should be in the format of "'value1','value2','value3',value4"#
# pay attention to the single quotes around the values                                     #
############################################################################################

# select_username() 
############################################################################################
# select one user through username                                                         #
# arguments for select_username() is username                                              #
# e.g select_username("admin")                                                             #
# the called function above equals to the following SQL statement                          #
# "SELECT * FROM account WHERE username = 'admin'"                                         # 
############################################################################################          

# update()
############################################################################################
# updating the score of a user                                                             #
# arguments for update() is table_name, column_name, value, condition                      #
# condition should be in the format of "column_name=value" like "id=1" or "username=xxx"   #
# statement = "UPDATE {table_name} SET {column_name} = {value} WHERE {condition}"          #
# e.g update("account", "password", 'admin123', "username=admin")                          #
# the called function above equals to the following SQL statement                          #
# "UPDATE account SET password = admin123 WHERE username=admin"                            #
# e.g update("account", "score", 200,"id=1")                                               #
# the called function above equals to the following SQL statement                          #
# "UPDATE account SET score = 200 WHERE id=1"                                              #
############################################################################################

# select_id()
############################################################################################
# selecting a user through id                                                              #
# arguments for select_id() is table_name, id, [column]                                    #
# e.g select_id("account",1,"score")                                                       #
# the called function above equals to the following SQL statement                          #
# "SELECT score FROM account WHERE id=1"                                                   #
# e.g select_id("account",1)                                                               #
# the called function above equals to the following SQL statement                          #
# "SELECT * FROM account WHERE id=1"                                                       #
# it returns a tuple of the information of the user                                        #
# it can also be used to get info from other tables                                        #
# e.g select_id("QUESTION_ACCOUNT",1)                                                      #
# e.g select_id("QUESTION_BLANK",1,"word")                                                 #
############################################################################################

# delete()
############################################################################################
# deleting a user from the database                                                        #
# arguments for delete() is table_name, condition                                          #
# condition should be in the format of "column_name=value" like "id=1" or "username=xxx"   #
# e.g delete("account", "id=1")                                                            #
# the called function above equals to the following SQL statement                          #
# "DELETE FROM account WHERE id=1"                                                         #
# e.g delete("account", "username=xinyu")                                                  #
# the called function above equals to the following SQL statement                          #
# "DELETE FROM account WHERE username=xinyu"                                               #
############################################################################################

# select_all()
############################################################################################
# selecting all users from the database                                                    #
# arguments for select_all() is table_name                                                 #
# e.g select_all("account")                                                                #
# the called function above equals to the following SQL statement                          #
# "SELECT * FROM account"                                                                  #
# it returns a list of tuple of all the users in the database                              #
# e.g [(1, 'admin', 'admin123', 'admin', 0), (2, 'ahmed', 'ahmed123', 'user', 100)]       #
############################################################################################
# select_all("account")

# insert_secure_question
############################################################################################
# inserting secure questions and answers for a user,when creating a new user               #
# arguments for insert_secure_question() is username, secure_question1,answer1, secure_question2,answer2 #
# need to "from user_crud_func import insert_secure_question" before calling the function  #
# the secure questions and answers are stored in the ACCOUNT table of the database         #
# e.g insert_secure_question("ahmed", "What is your favorite color?","red", "What is your favorite food?","pizza") #
# the called function above equals to the following SQL statement                          #
# "UPDATE ACCOUNT SET secure_question1 = 'What is your favorite color?:red', secure_question2 = 'What is your favorite food?:pizza' WHERE username = 'ahmed'" #
# the function returns nothing but print "inserted secure questions for {username} successfully"             #
############################################################################################

# show_secure_question
###########################################################################################
# showing secure questions for a user when the user forgets the password in reset password#
# arguments for show_secure_question() is username                                        #
# need to "from user_crud_func import show_secure_question" before calling the function   #
# the secure questions and answers are stored in the ACCOUNT table of the database        #
# e.g show_secure_question("ahmed")                                                       #
# the called function above equals to the following SQL statement                         #
# "SELECT secure_question1,secure_question2 FROM account WHERE username = 'ahmed'"        #
# the function returns a list of the secure questions and answers                         #
# e.g ["What is your favorite color?","What is your favorite food?"]                      #
###########################################################################################

#check_secure_question
###########################################################################################
# checking the secure questions and answers for a user when the user resets the password  #
# arguments for check_secure_question() is username, secure_questions, answers            #
# secure_questions is list of of 2 questions and answers is lists of 2 answers            #
# need to "from user_crud_func import check_secure_question" before calling the function  #
# e.g check_secure_question("ahmed", ["What is your favorite color?","What is your favorite food?"], ["red","pizza"]) #
# the called function above equals to the following SQL statement                         #
# "SELECT secure_question1,secure_question2 FROM account WHERE username = 'ahmed'"        #
# the function returns True if the answers are correct, False otherwise                   #
###########################################################################################

# auth()
############################################################################################
# authorizing a user                                                                       #
# arguments for auth() is username, password                                               #
# if the user is authenticated, return True, "Authenticated"                               #
# if the user is not authenticated, return False, "User not found"                         #
# if the user is found but the password is incorrect, return False, "Password incorrect"   #
# auth("ahmed", "ahmed123")                                                                #
############################################################################################
def auth(username, password) -> tuple: 
    # return a tuple, tuple[0] is the boolean, tuple[1] is the information
    statement_auth="SELECT Username,Password FROM account"
    rows = cursor.execute(statement_auth)
    # print(rows)
    result = rows.fetchall()
    print(result)
    for row in result:
        print(f"Checking username: {row[0]}, stored hash: {row[1]}")
        if row[0] == username and row[1] == password:
            print(f"User {row[0]} authenticated")
            return True, "Authenticated"
        elif row[0] == username:
            print(f"User {row[0]} Password incorrect")
            return False, "Password incorrect"
    
    print(f"User {username} not found")
    return False, "User not found"

# sign_up()
############################################################################################
# signing up a new user                                                                    #
# arguments for sign_up() is username, password                                            #
# if the user already exists, return False, "User already exists"                          #
# if the user does not exist, create the user and return True, "User created"              #
# sign_up("eddie12", "p@ssword1", "What is your favorite color?", "red", "What is your favorite food?", "pizza")                                                           #
# The called function above equals to the following SQL statement                          #
# "INSERT INTO ACCOUNT(username,password,role,score) VALUES ('ahmed','ahmed123','user',0)" #
############################################################################################
def sign_up(username, password, secure_question1, answer1, secure_question2, answer2) -> tuple: # return a tuple, tuple[0] is the boolean, tuple[1] is the information
    users = select_all("account", "username")
    # print(users)
    for user in users:
        if user[0] == username:
            print(f"User {username} already exists")
            return False, "User already exists"
    if len(username) < 4:
        return False, "Username should be at least 4 characters"
    if len(password) < 6:
        return False, "Password should be at least 6 characters"
    if not check_password(password):
        return False, "Password should contain at least one uppercase letter, one lowercase letter, one digit and one special character"
    if answer1 == "" or answer2 == "":
        return False, "Answers should not be empty"
    
    create("account", "username,password,role,score,secure_question1,secure_question2", f"'{username}','{password}','user',0,'{secure_question1}:{answer1}', '{secure_question2}:{answer2}'") 
    return True, "User created"

def check_password(password):
    if len(password) < 6:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in "!=/@#$%^&*()-+" for char in password):
        return False
    return True

# update_score()
############################################################################################
# updating the score of a user                                                             #
# arguments for update_score() is index, score, correct_questions, incorrect_questions     #
# correct_questions and incorrect_questions are lists of questions                         #
# questions list should be in the format of ["question_id","question_id","question3_id"]   #
# question list can be empty                                                               #
# index can be the id of the user or the username of the user                              #
# e.g update_score(1, 100, ["1","2","3"], ["4","5","6"])                                   #
# e.g update_score("ahmed", 100, ["1","2","3"], ["4","5","6"])                             #
# The called function above equals to the following SQL statement                          #
# "INSERT INTO QUESTION_ACCOUNT(id,correct_questions,incorrect_questions) VALUES {100, ["1","2","3"], ["4","5","6"]}" 
# if the user is found, update the score and the correct and incorrect questions           #
# return True, "Score updated, correct and incorrect questions updated"                    #
# if the score is not an integer, return False, "Score should be an integer"               #
############################################################################################
def update_score(index, score,correct_questions:list=None,incorrect_questions:list=None) -> tuple: # return a tuple, tuple[0] is the boolean, tuple[1] is the information
    if not isinstance(score, int):
        return False, "Score should be an integer"
    if isinstance(index, int):
        account_id=index
        try:
            old_score = select_id("account", account_id, "score")[0]
        except:
            print(f"User ID {index} not found")
            return False, "User not found"
    else:
        try:
            old_score = select_username(index, "score")[0]
            account_id = select_username(index, "id")[0]
        except:
            print(f"User Name {index} not found")
            return False, "User not found"
    score += old_score
    print("the old score is", old_score)
    print("the new score is", score)
    # update the score of the user with the new score in the ACCOUNT table of database
    update("ACCOUNT", "score", score, f"id='{account_id}'")
    # if there is nothing in the list, set it to empty list
    if not correct_questions:
        correct_questions = []
    if not incorrect_questions:
        incorrect_questions = []
    correct_questions = list(set(correct_questions)) # remove duplicates
    incorrect_questions = list(set(incorrect_questions)) # remove duplicates
    # update the correct and incorrect questions of the user in the QUESTION_ACCOUNT table of database
    # the correct and incorrect questions are stored as a string in the database
    value = f'({account_id},"{correct_questions}","{incorrect_questions}")' 
    table_name = "QUESTION_ACCOUNT"
    column_name = "account_id,correct_questions,incorrect_questions"
    insert(table_name,column_name,value)
    return True, "Score updated, correct and incorrect questions updated"


def update_score_table(index,table, score,correct_questions:list=None,incorrect_questions:list=None) -> tuple: # return a tuple, tuple[0] is the boolean, tuple[1] is the information
    if not isinstance(score, int):
        return False, "Score should be an integer"
    if isinstance(index, int):
        account_id=index
        try:
            old_score = select_id("account", account_id, "score")[0]
        except:
            print(f"User ID {index} not found")
            return False, "User not found"
    else:
        try:
            old_score = select_username(index, "score")[0]
            account_id = select_username(index, "id")[0]
        except:
            print(f"User Name {index} not found")
            return False, "User not found"
    score += old_score
    print("the old score is", old_score)
    print("the new score is", score)
    # update the score of the user with the new score in the ACCOUNT table of database
    update("ACCOUNT", "score", score, f"id='{account_id}'")
    # if there is nothing in the list, set it to empty list
    if not correct_questions:
        correct_questions = []
    if not incorrect_questions:
        incorrect_questions = []
    correct_questions = list(set(correct_questions)) # remove duplicates
    incorrect_questions = list(set(incorrect_questions)) # remove duplicates
    # update the correct and incorrect questions of the user in the QUESTION_ACCOUNT table of database
    # the correct and incorrect questions are stored as a string in the database
    value = f'({account_id},"{correct_questions}","{incorrect_questions}")' 
    table_name = table
    column_name = "account_id,correct_questions,incorrect_questions"
    insert(table_name,column_name,value)
    return True, "Score updated, correct and incorrect questions updated"


#update_score("xinyu", 100, ["1","2","3"], ["4","5","6"])
############################################################################################
# reading all data about one user from the QUESTION_ACCOUNT table using user_id            #
# arguments for read_question_account() is user_id                                         #
# e.g read_question_account(1)                                                             #
# The called function above equals to the following SQL statement                          #
# "SELECT * FROM QUESTION_ACCOUNT, ACCOUNT WHERE QUESTION_ACCOUNT.account_id = ACCOUNT.id AND ACCOUNT.id=1" #
# return the username, correct questions and incorrect questions of the user               #
# in a dictionary format                                                                   #
# e.g {"username":"ahmed","correct_questions":["1","2","3"],"incorrect_questions":["4","5","6"]} #
############################################################################################
def read_question_account(id:int) -> dict:
    statement = f"SELECT * FROM QUESTION_ACCOUNT, ACCOUNT WHERE QUESTION_ACCOUNT.account_id = ACCOUNT.id AND ACCOUNT.id={id}"
    rows = cursor.execute(statement)
    result = rows.fetchall()
    correct_list=[]
    incorrect_list=[]
    # get all the information of the user under the condition
    for i in result:
        [qa_id, account_id, correct_questions, incorrect_questions, account_id, username, password, role, score] = i
        # get the correct and incorrect questions of the user of each record and add them to the list
        correct_list+=eval(correct_questions)
        incorrect_list+=eval(incorrect_questions)
    # remove duplicates
    correct_list=list(set(correct_list)) 
    incorrect_list=list(set(incorrect_list))
    # build a dictionary for the user
    user_dict = {"username":username,"correct_questions":correct_list,"incorrect_questions":incorrect_list}
    print(user_dict)
    return user_dict


"""
how to build functions for the following functionalities:

document my functions about how to use them.
you can tell me where you need clarification.
1. CRUD for questions
    1.Update questions
    2.delete questions
3. Forget password
4. Admin dashboard(delete user)
5. rank func

"""
