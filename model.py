# file for the model class
# because we are using sqlite3 to store the data, we don't need id in the json file
import random
from usermod import select_id, execute
import sqlite3
database = './database/database.db'
connection = sqlite3.connect(database,check_same_thread=False) # create the file if it does not exist 
cursor = connection.cursor() # cursor is used to interact with the database 

class Word:
    def __init__(self,word,phonetics,correct,incorrect_list,word_example):
        self.word = word
        self.phonetics = phonetics
        self.correct = correct
        self.incorrect_list = incorrect_list
        self.word_example = word_example
    def __str__(self):
        return f'{self.word} {self.phonetics} {self.correct} {self.incorrect_list} {self.word_example}'
    def choose_word(self,data):
        # remove the right word from the list of words where the wrong answers are chosen
        # before the word is removed, we need to make a copy of the list, so that the original list is not modified
        data_copy = data.copy()
        data_copy.remove(self.word)
        self.incorrect_list = random.sample(data_copy, k=3)
        self.correct = self.word
        list_of_word = self.word_example.split(" ")
        for i in list_of_word:
            # find the word in the sentence
            if i == self.word:
                index = list_of_word.index(i)
                # replace the word with blank of the same length
                list_of_word = list_of_word[:index] + ["_" * len(self.word)] + list_of_word[index+1:]
        self.word_example = " ".join(list_of_word)
############################################################################################################
# get a word from the table using the word                                                                 #
# the function in the model.py file is select_word(table_name:str, word:str, column_name="*") -> tuple:    #
# need to "from model import select_word"                                                                  #
# take 3 arguments: table_name, word, column_name                                                          #
# e.g. select_word("QUESTION_DEFINITION", "apple")                                                         #
# the called function above equals to the following SQL statement                                          #
# SELECT * FROM QUESTION_DEFINITION WHERE word = 'apple'                                                   #
# the function returns a tuple of the word selected                                                        #
# e.g. (1, 'apple', 'A round fruit with seeds.', '["A type of bird.", "An underwater creature.", "A mode of transportation."]', 1, 'I enjoy eating a juicy apple for breakfast.')#
############################################################################################################
def select_word(table_name:str, word:str, column_name="*") -> tuple:
    rows = cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE word = '{word}'")
    result = rows.fetchone()
    # print(result)
    return result

############################################################################################################
# get a word from the table using the id or word and return a dictionary                                   #
# the function in the model.py file is get_question_dict(table_name, index) -> dict:                       #
# need to "from model import get_question_dict" before calling the function                                #
# take 2 arguments: table_name, index                                                                      #
# index can be string of word or int of word id.                                                           #
# e.g. get_question_dict("QUESTION_DEFINITION", "apple")                                                   #
# the called function above equals to the following SQL statement                                          #
# SELECT * FROM QUESTION_DEFINITION WHERE word = 'apple'                                                   #
# the function returns a dictionary of the word selected                                                   #
# {'id': 1, 'word': 'apple', 'definition': 'A round fruit with seeds.', 'incorrect_list': '["A type of bird.", "An underwater creature.", "A mode of transportation."]', 'correct': 1, 'example': 'I enjoy eating a juicy apple for breakfast.'}#
############################################################################################################
def get_question_dict(table_name, index) -> dict:
    if isinstance(index, str):
        try:
            id = select_word("QUESTION_DEFINITION", index)[0]
        except:
            print(f"Word {index} not found")
    else:
        id = index
    # get the question from the table
    question = select_id(table_name, id)
    # put it in a dictionary
    question_dict = {
        "id": question[0],
        "word": question[1],
        "correct": question[2],
        "incorrect_list": question[3],
        "weight": question[4],
        "phonetics": question[5],
        "example": question[6]
        
    }
    # print(question_dict)
    print("Question dictionary created")
    return question_dict
#################################################################################################
import secrets
import json

def generate_question_list(IDrange,number_of_questions,table_name):
    questions_list = []
    questions_id = []

    while len(questions_list) < number_of_questions:
        num = 0
        while num == 0 or num in questions_id:
            num = secrets.randbelow(IDrange) + 1

        questions_id.append(num)
        question_data = get_question_dict(table_name, num)

        question_dict = {
            'question': question_data.get('example'),
            'incorrect_list': json.loads(question_data.get('incorrect_list')),
            'id': question_data.get('id'),
            'correct': question_data.get('correct')
        }

        questions_list.append(question_dict)

    questions_list_json = json.dumps(questions_list)
    return questions_list_json
