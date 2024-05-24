import sqlite3, json,requests
from pathlib import Path
from model import Word
from usermod import create_account_table
from database import secure_question_list
database = './database/database.db'
connection = sqlite3.connect(database,check_same_thread=False) # create the file if it does not exist 
cursor = connection.cursor() # cursor is used to interact with the database 

def execute(statement):
    cursor.execute(statement) 
    connection.commit()

def drop(table_name):
    statement_drop = f"DROP TABLE IF EXISTS {table_name.upper()}" 
    execute(statement_drop) #  delete

# a function to get the meaning of the word
# the function takes in the word and the data from the json file
def get_meaning_phone(word,data):
    # using the api of dictionary to get information about the word
    response_of_meaning = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    if response_of_meaning.status_code == 200:
        word_original_json = response_of_meaning.json()[0]
        # get the word
        my_word = word_original_json["word"]
        # get the phonetics
        if word_original_json["phonetics"][0]["audio"] != "":
            word_phonetics = word_original_json["phonetics"][0]["audio"]
        elif word_original_json["phonetics"][1]["audio"] != "":
            word_phonetics = word_original_json["phonetics"][1]["audio"]
        else:
            word_phonetics = ""
            print("No audio available")
        # get the meaning
        for word in data:
            if word["word"] == my_word:
                word_meaning = word["correct"]
                word_incorrect_list = word["incorrect"]
                word_example = word["example"]
                break
        return my_word,word_phonetics,word_meaning,word_incorrect_list,word_example
    
# get the existing words in the json file
def get_existing_words(path):
    with open(path,"r",encoding="utf-8") as file:
        data = json.load(file)
        word_list = [word["word"] for word in data]
        return word_list

def create_secure_question_table():
    drop("SECURE_QUESTION")
    statement_secure_question = """CREATE TABLE IF NOT EXISTS SECURE_QUESTION
                    (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL);"""
    execute(statement_secure_question)
    for question in secure_question_list.secure_questions:
        statement = f"""INSERT INTO SECURE_QUESTION
                        (question) 
                        VALUES ('{question}')"""
        execute(statement)

############################################################################################################
# get all the secure questions from the database                                                           #
# the function in the manage.py file is return_all_secure_question() -> list:                              #
# need to "from manage import return_all_secure_question" before calling the function                      #
# take no arguments                                                                                        #
# e.g. return_all_secure_question()                                                                        #
# the called function above equals to the following SQL statement                                          #
# SELECT * FROM SECURE_QUESTION                                                                            #
# the function returns a list of all the secure questions                                                  #
# e.g. [(1, 'What is your favorite color?'), (2, 'What is your favorite food?'), (3, 'What is your favorite movie?'), (4, 'What is your favorite book?'), (5, 'What is your favorite song?'), (6, 'What name is your favorite pet?'), (7, 'What is your favorite game?'), (8, 'What is your favorite TV show?'), (9, 'What is your favorite car?'), (10, 'Where was you born?'), (11, 'Which city did you parents met?')]#
############################################################################################################
def return_all_secure_question()->list:
    rows = cursor.execute(f'SELECT * FROM SECURE_QUESTION') 
    result = rows.fetchall()
    print("Return_all_secure_question()",result)
    return result

if __name__ == "__main__":
    create_secure_question_table()
    create_account_table()
    # drop everything in the database before adding new tables
    drop("QUESTION_ACCOUNT")
    question_definition = "QUESTION_DEFINITION"
    question_blank = "QUESTION_BLANK"
    question_table_list = [question_definition, question_blank]
    [drop(table) for table in question_table_list]
    # create a table for the question_defintion
    for table in question_table_list:
        statement_question_table = f"""CREATE TABLE IF NOT EXISTS {table}
                    (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    word  TEXT NOT NULL UNIQUE,
                    correct TEXT NOT NULL,
                    incorrect TEXT NOT NULL,
                    weight INTEGER DEFAULT 1,
                    phonetics_url TEXT,
                    example TEXT);"""
        execute(statement_question_table)

    # an  list to store the words themselves
    list_of_words= get_existing_words("database/data.json")
    # get the words we have in the json file, this words are not processed, with only the word, and 4 meanings, 1 correct and 3 incorrect
    with open("database/data.json","r",encoding="utf-8") as file:
        data = json.load(file)
        for word in data:
            word_tuple = get_meaning_phone(word["word"],data)
            # make it into an object
            word_for_question = Word(word_tuple[0],word_tuple[1],word_tuple[2],word_tuple[3],word_tuple[4])
            # make it into a dictionary for json
            word_for_question_dictionary = word_for_question.__dict__
            # append the dictionary into table question_definition of database
            statement= f"""INSERT INTO {question_definition}
                        (word, correct, incorrect,phonetics_url, example) 
                        VALUES ('{word_for_question_dictionary['word']}', 
                            '{word_for_question_dictionary['correct']}', 
                            '{json.dumps(word_for_question_dictionary['incorrect_list'])}',
                            '{word_for_question_dictionary['phonetics']}', 
                            "{word_for_question_dictionary['word_example']}")"""
            execute(statement)

            # second type of question, fill in the blank
            # make a sentence with the word picked out, and replace the word with blank
            word_blank = Word(word_tuple[0],word_tuple[1],word_tuple[2],word_tuple[3],word_tuple[4])
            # randomly choose 3 words from the list of words to be the incorrect answers
            Word.choose_word(word_blank,list_of_words)
            word_blank_dictionary = word_blank.__dict__
            statement= f"""INSERT INTO {question_blank}
                        (word, correct, incorrect, phonetics_url,example) 
                        VALUES ('{word_blank_dictionary['word']}', 
                            '{word_blank_dictionary['correct']}', 
                            '{json.dumps(word_blank_dictionary['incorrect_list'])}',
                            '{word_for_question_dictionary['phonetics']}',  
                            "{word_blank_dictionary['word_example']}")"""
            execute(statement)
    # create an associative table for the question_account
    statement_question_account = f"""CREATE TABLE IF NOT EXISTS QUESTION_ACCOUNT
                    (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id  INT NOT NULL,
                    correct_questions INT NOT NULL,
                    incorrect_questions INT NOT NULL,
                    FOREIGN KEY(account_id) REFERENCES ACCOUNT(id),
                    FOREIGN KEY(correct_questions) REFERENCES {question_definition}(id),
                    FOREIGN KEY(incorrect_questions) REFERENCES {question_definition}(id));"""
    execute(statement_question_account)
    print("Database created")