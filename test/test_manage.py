import unittest
from manage import *
from unittest import mock
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

def test_execute(mock_connection, mock_cursor):
    statement = "CREATE TABLE test (id INTEGER)"
    execute(statement)
    mock_cursor.execute.assert_called_once_with(statement)
    mock_connection.commit.assert_called_once()

def test_drop(mock_connection, mock_cursor):
    table_name = "test"
    drop(table_name)
    mock_cursor.execute.assert_called_once_with(f"DROP TABLE IF EXISTS {table_name.upper()}")
    mock_connection.commit.assert_called_once()

def test_get_meaning_phone():
    word = "apple"
    data = [
        {"word": "apple", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate an apple."},
        {"word": "banana", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate a banana."},
    ]
    result = get_meaning_phone(word, data)
    expected_result = ("apple", "", "A fruit", ["A color", "A car", "A movie"], "I ate an apple.")
    assert result == expected_result

def test_get_existing_words():
    path = "database/data.json"
    result = get_existing_words(path)
    expected_result = ["apple", "banana"]
    assert result[0:2] == expected_result

'''
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
'''

def test_create_secure_question_table(mock_connection, mock_cursor):
    with open("database/secure_question_list.py") as f:
        secure_question_list = f.read()
        length_of_questions_to_be_inserted = len(secure_question_list)
    create_secure_question_table()
    mock_cursor.execute.call_count == length_of_questions_to_be_inserted + 1


def test_return_all_secure_question(mock_cursor):
    return_all_secure_question()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM SECURE_QUESTION")

def test_change_weight_for_table(mock_cursor):
    table_name = "QUESTION_DEFINITION"
    word = "apple"
    change_weight_for_table(table_name, 1, word)
    mock_cursor.execute.assert_called_once_with(f"UPDATE {table_name} SET weight = 1 WHERE word = '{word}'")

def test_replace_s():
    word_dict = {"word": "apple", "phonetics": "ˈæpəl", "correct": "A type of bird.'s", "incorrect": ["A type of bird.'s", "An underwater creature.'s", "A mode of transportation.'s"], "example": "I enjoy eating a juicy apple for breakfast.'s"}
    result = replace_s(word_dict)
    expected_result = {"word": "apple", "phonetics": "ˈæpəl", "correct": "A type of bird.’s", "incorrect": ["A type of bird.’s", "An underwater creature.’s", "A mode of transportation.’s"], "example": "I enjoy eating a juicy apple for breakfast.’s"}
    assert result == expected_result
    