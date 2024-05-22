import unittest
from manage import *

class TestManage(unittest.TestCase):
    def setUp(self):
        # Set up the database connection
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def tearDown(self):
        # Close the database connection
        self.connection.close()

    def test_execute(self):
        # Test the execute function
        statement = "CREATE TABLE IF NOT EXISTS TEST_TABLE (id INTEGER PRIMARY KEY, name TEXT)"
        execute(statement)
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TEST_TABLE'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_drop(self):
        # Test the drop function
        table_name = "TEST_TABLE"
        drop(table_name)
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TEST_TABLE'")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_get_meaning_phone(self):
        # Test the get_meaning_phone function
        word = "apple"
        data = [
            {"word": "apple", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate an apple."},
            {"word": "banana", "correct": "A fruit", "incorrect": ["A color", "A car", "A movie"], "example": "I ate a banana."},
        ]
        result = get_meaning_phone(word, data)
        expected_result = ("apple", "", "A fruit", ["A color", "A car", "A movie"], "I ate an apple.")
        self.assertEqual(result, expected_result)

    def test_get_existing_words(self):
        # Test the get_existing_words function
        path = "database/data.json"
        result = get_existing_words(path)
        expected_result = ["apple", "banana"]
        self.assertEqual(result, expected_result)

    def test_create_secure_question_table(self):
        # Test the create_secure_question_table function
        drop("SECURE_QUESTION")
        create_secure_question_table()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SECURE_QUESTION'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_return_all_secure_question(self):
        # Test the return_all_secure_question function
        drop("SECURE_QUESTION")
        create_secure_question_table()
        result = return_all_secure_question()
        expected_result = [
            (1, "What is your favorite color?"),
            (2, "What is your favorite food?"),
            (3, "What is your favorite movie?"),
            (4, "What is your favorite book?"),
            (5, "What is your favorite song?"),
            (6, "What name is your favorite pet?"),
            (7, "What is your favorite game?"),
            (8, "What is your favorite TV show?"),
            (9, "What is your favorite car?"),
            (10, "Where were you born?"),
            (11, "Which city did your parents meet?"),
        ]
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()