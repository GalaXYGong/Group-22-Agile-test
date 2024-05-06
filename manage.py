import sqlite3, json,requests
from pathlib import Path
from model import Word
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

if __name__ == "__main__":
    # drop everything in the database before adding new tables
    question_definition = "QUESTION_DEFINITION"
    question_blank = "QUESTION_BLANK"
    question_table_list = [question_definition, question_blank]
    [drop(table) for table in question_table_list]
    # incorrect = ['apple', 'banana', 'cherry']
    # json_str = json.dumps(incorrect)
    # create a table for the question_defintion
    for table in question_table_list:
        statement_question_table = f"""CREATE TABLE IF NOT EXISTS {table}
                    (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    word  TEXT NOT NULL UNIQUE,
                    correct TEXT NOT NULL,
                    incorrect TEXT NOT NULL,
                    weight INTEGER DEFAULT 1,
                    example TEXT);"""
        execute(statement_question_table)

    # statement_insert = f"INSERT INTO QUESTION(word, correct, incorrect, example) VALUES ('apple', 'A round fruit with seeds.', '{json_str}', 'I enjoy eating a juicy apple for breakfast.')"
    # execute(statement_insert)

    # an  list to store the words themselves
    list_of_words= get_existing_words("data.json")
    # get the words we have in the json file, this words are not processed, with only the word, and 4 meanings, 1 correct and 3 incorrect
    with open("data.json","r",encoding="utf-8") as file:
        data = json.load(file)
        for word in data:
            word_tuple = get_meaning_phone(word["word"],data)
            # make it into an object
            word_for_question = Word(word_tuple[0],word_tuple[1],word_tuple[2],word_tuple[3],word_tuple[4])
            # make it into a dictionary for json
            word_for_question_dictionary = word_for_question.__dict__
            # append the dictionary into table question_definition of database
            statement= f"""INSERT INTO {question_definition}
                        (word, correct, incorrect, example) 
                        VALUES ('{word_for_question_dictionary['word']}', 
                            '{word_for_question_dictionary['correct']}', 
                            '{json.dumps(word_for_question_dictionary['incorrect_list'])}', 
                            "{word_for_question_dictionary['word_example']}")"""
            execute(statement)

            # second type of question, fill in the blank
            # make a sentence with the word picked out, and replace the word with blank
            word_blank = Word(word_tuple[0],word_tuple[1],word_tuple[2],word_tuple[3],word_tuple[4])
            # randomly choose 3 words from the list of words to be the incorrect answers
            Word.choose_word(word_blank,list_of_words)
            word_blank_dictionary = word_blank.__dict__
            statement= f"""INSERT INTO {question_blank}
                        (word, correct, incorrect, example) 
                        VALUES ('{word_blank_dictionary['word']}', 
                            '{word_blank_dictionary['correct']}', 
                            '{json.dumps(word_blank_dictionary['incorrect_list'])}', 
                            "{word_blank_dictionary['word_example']}")"""
            execute(statement)
