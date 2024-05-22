import unittest
from model import Word, select_word, get_question_dict

class TestWord(unittest.TestCase):
    def setUp(self):
        self.word = Word("apple", "ˈæpəl", 1, ["A type of bird.", "An underwater creature.", "A mode of transportation."], "I enjoy eating a juicy apple for breakfast.")

    def test_init(self):
        self.assertEqual(self.word.word, "apple")
        self.assertEqual(self.word.phonetics, "ˈæpəl")
        self.assertEqual(self.word.correct, 1)
        self.assertEqual(self.word.incorrect_list, ["A type of bird.", "An underwater creature.", "A mode of transportation."])
        self.assertEqual(self.word.word_example, "I enjoy eating a juicy apple for breakfast.")

    def test_str(self):
        self.assertEqual(str(self.word), "apple ˈæpəl 1 ['A type of bird.', 'An underwater creature.', 'A mode of transportation.'] I enjoy eating a juicy apple for breakfast.")

    def test_choose_word(self):
        data = ["apple", "banana", "cherry", "durian"]
        self.word.choose_word(data)
        self.assertEqual(self.word.correct, "apple")
        self.assertEqual(len(self.word.incorrect_list), 3)
        self.assertNotIn("apple", self.word.incorrect_list)
        self.assertIn(self.word.incorrect_list[0], data)
        self.assertIn(self.word.incorrect_list[1], data)
        self.assertIn(self.word.incorrect_list[2], data)

class TestSelectWord(unittest.TestCase):
    def test_select_word(self):
        result = select_word("QUESTION_DEFINITION", "apple")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], "apple")
        self.assertEqual(result[2], "A round fruit with seeds.")
        self.assertEqual(result[3], '["A type of bird.", "An underwater creature.", "A mode of transportation."]')
        self.assertEqual(result[4], 1)
        self.assertEqual(result[5], "I enjoy eating a juicy apple for breakfast.")

class TestGetQuestionDict(unittest.TestCase):
    def test_get_question_dict_with_word(self):
        result = get_question_dict("QUESTION_DEFINITION", "apple")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 7)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["word"], "apple")
        self.assertEqual(result["correct"], 1)
        self.assertEqual(result["incorrect_list"], '["A type of bird.", "An underwater creature.", "A mode of transportation."]')
        self.assertEqual(result["weight"], 1)
        self.assertEqual(result["phonetics"], "ˈæpəl")
        self.assertEqual(result["example"], "I enjoy eating a juicy apple for breakfast.")

    def test_get_question_dict_with_id(self):
        result = get_question_dict("QUESTION_DEFINITION", 1)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 7)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["word"], "apple")
        self.assertEqual(result["correct"], 1)
        self.assertEqual(result["incorrect_list"], '["A type of bird.", "An underwater creature.", "A mode of transportation."]')
        self.assertEqual(result["weight"], 1)
        self.assertEqual(result["phonetics"], "ˈæpəl")
        self.assertEqual(result["example"], "I enjoy eating a juicy apple for breakfast.")

if __name__ == "__main__":
    unittest.main()