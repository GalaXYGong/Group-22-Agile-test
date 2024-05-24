import unittest
from model import *
from manage import *
from unittest import mock
import user_crud_func
import sqlite3
import pytest
@pytest.fixture
def mock_cursor():
    with mock.patch('manage.cursor') as mock_cursor:
        yield mock_cursor

@pytest.fixture
def mock_connection():
    with mock.patch('manage.connection') as mock_connection:
        yield mock_connection

def test_select_word():
    word_test = "apple"
    data = [
        {"word": "apple", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate an apple."},
        {"word": "banana", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate a banana."},
    ]
    table = "QUESTION_DEFINITION"
    drop(table)
    statement_question_table = f"""CREATE TABLE IF NOT EXISTS {table}
                    (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    word  TEXT NOT NULL UNIQUE,
                    correct TEXT NOT NULL,
                    incorrect TEXT NOT NULL,
                    weight INTEGER DEFAULT 1,
                    phonetics_url TEXT,
                    example TEXT);"""
    execute(statement_question_table)
    for word in data:
        word = replace_s(word)
        word_tuple = get_meaning_phone(word["word"],data)
        # make it into an object
        word_for_question = Word(word_tuple[0],word_tuple[1],word_tuple[2],word_tuple[3],word_tuple[4])
        # make it into a dictionary for json
        word_for_question_dictionary = word_for_question.__dict__
        # append the dictionary into table question_definition of database
        statement= f"""INSERT INTO {table}
                    (word, correct, incorrect,phonetics_url, example) 
                    VALUES ('{word_for_question_dictionary['word']}', 
                        '{word_for_question_dictionary['correct']}', 
                        '{json.dumps(word_for_question_dictionary['incorrect_list'])}',
                        '{word_for_question_dictionary['phonetics']}', 
                        "{word_for_question_dictionary['word_example']}")"""
        execute(statement)
    result = select_word(table,word_test)[1:]
    expected_result = ('apple', 'A fruit', '["A color", "A car", "A movie"]', 1, '', 'I ate an apple.')
    assert result == expected_result


def test_get_question_dict():
    word_test = "apple"
    data = [
        {"word": "apple", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate an apple."},
        {"word": "banana", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate a banana."},
    ]
    table = "QUESTION_DEFINITION"
    drop(table)
    statement_question_table = f"""CREATE TABLE IF NOT EXISTS {table}
                    (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    word  TEXT NOT NULL UNIQUE,
                    correct TEXT NOT NULL,
                    incorrect TEXT NOT NULL,
                    weight INTEGER DEFAULT 1,
                    phonetics_url TEXT,
                    example TEXT);"""
    execute(statement_question_table)
    for word in data:
        word = replace_s(word)
        word_tuple = get_meaning_phone(word["word"],data)
        # make it into an object
        word_for_question = Word(word_tuple[0],word_tuple[1],word_tuple[2],word_tuple[3],word_tuple[4])
        # make it into a dictionary for json
        word_for_question_dictionary = word_for_question.__dict__
        # append the dictionary into table question_definition of database
        statement= f"""INSERT INTO {table}
                    (word, correct, incorrect,phonetics_url, example) 
                    VALUES ('{word_for_question_dictionary['word']}', 
                        '{word_for_question_dictionary['correct']}', 
                        '{json.dumps(word_for_question_dictionary['incorrect_list'])}',
                        '{word_for_question_dictionary['phonetics']}', 
                        "{word_for_question_dictionary['word_example']}")"""
        execute(statement)
    result = get_question_dict(table,1)
    expected_result = {'id': 1, 'word': 'apple', 'correct': 'A fruit', 'incorrect_list': '["A color", "A car", "A movie"]', 'weight': 1, 'phonetics': '', 'example': 'I ate an apple.'}
    print(result)
    print(expected_result)
    assert result == expected_result

def test_generate_question_list():
    word_test = "apple"
    data = [
        {"word": "apple", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate an apple."},
        {"word": "banana", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate a banana."},
    ]
    table = "QUESTION_DEFINITION"
    drop(table)
    statement_question_table = f"""CREATE TABLE IF NOT EXISTS {table}
                    (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    word  TEXT NOT NULL UNIQUE,
                    correct TEXT NOT NULL,
                    incorrect TEXT NOT NULL,
                    weight INTEGER DEFAULT 1,
                    phonetics_url TEXT,
                    example TEXT);"""
    execute(statement_question_table)
    for word in data:
        word = replace_s(word)
        word_tuple = get_meaning_phone(word["word"],data)
        # make it into an object
        word_for_question = Word(word_tuple[0],word_tuple[1],word_tuple[2],word_tuple[3],word_tuple[4])
        # make it into a dictionary for json
        word_for_question_dictionary = word_for_question.__dict__
        # append the dictionary into table question_definition of database
        statement= f"""INSERT INTO {table}
                    (word, correct, incorrect,phonetics_url, example) 
                    VALUES ('{word_for_question_dictionary['word']}', 
                        '{word_for_question_dictionary['correct']}', 
                        '{json.dumps(word_for_question_dictionary['incorrect_list'])}',
                        '{word_for_question_dictionary['phonetics']}', 
                        "{word_for_question_dictionary['word_example']}")"""
        execute(statement)
    result = generate_question_list(2,2,table)
    new_result = []
    for question in eval(result):
        question.pop('id')
        new_result.append(question)
    expected_result = '[{"question": "I ate a banana.", "incorrect_list": ["A color", "A car", "A movie"], "correct": "A fruit"},{"question": "I ate an apple.", "incorrect_list": ["A color", "A car", "A movie"], "correct": "A fruit"}]'
    expected_result= eval(expected_result)
    new_result= sorted(new_result,key = lambda x: x['question'])
    print(new_result)
    print(expected_result)
    assert new_result == expected_result
    drop(table)