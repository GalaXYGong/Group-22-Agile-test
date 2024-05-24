
# this is a trial file for testing the update_score function

# from user_crud_func import update_score, read_question_account, sign_up, select_all
# from usermod import insert_secure_question, show_secure_question, check_secure_question
# from manage import return_all_secure_question
# sign_up("eddie", "Eddie123@", "What is your favorite color?",'red',"What is your favorite food?","pizza")
# you can register a new user and update the score, then change the user name or id to test the function
# update_score("ahmed", 100, ["1","2","3"], ["4","5","6"])
# update_score(2, 100, ["1","2","3"], ["4","5","6"])
# read_question_account(2) 


# from usermod import select_id
# select_id("QUESTION_BLANK", 2)
# from model import select_word
# select_word("QUESTION_DEFINITION", "apple")
# from model import get_question_dict
# get_question_dict("QUESTION_DEFINITION", "banana")
# sign_up("xinyu", "xinyu1234")

# username = "xinyu"
# secure_question1 = "What is your favorite color?"
# answer1 = "red"
# secure_question2 = "What is your favorite food?"
# answer2 = "pizza"
# insert_secure_question(username, secure_question1,answer1, secure_question2,answer2)

# show_secure_question("ahmed")
# print(check_secure_question("xinyu", ["What is your favorite color?","What is your favorite food?"], ["red","pizza"]))
# print(check_secure_question("xinyu", ["What is your favorite color?","What is your favorite food?"], ["blue","pizza"]))
# print(check_secure_question("xinyu", ["What is your favorite?","What is your favorite food?"], ["red","pizza"]))
# print(check_secure_question("xinyu", ["What is your favorite color?","What is your favorite food?"], ["blue","apple"]))
# print(check_secure_question("ahmed", ["What is your favorite color?","What is your favorite food?"], ["red","apple"]))
# sign_up_with_questions("eddie", "eddie123", "What is your favorite color?",'red',"What is your favorite food?","pizza")


# 
# return_all_secure_question()

# sign_up_with_questions("eddie", "eddie123", "What is your favorite color?",'red',"What is your favorite food?","pizza")
# check_secure_question("eddie", ["What is your favorite color?","What is your favorite food?"], ["red","pizza"])

# from manage import get_existing_words
# word_list = get_existing_words("database/data.json")    
# print(", ".join(word_list))
# print(len(word_list))
# # 给我一个测重复的单词的方法
# # 从上述列表中获取单词，返回重复的单词

# list_without_duplicate = list(set(word_list))
# print(len(list_without_duplicate))
# # 打印出重复的单词
# for word in list_without_duplicate:
#     word_list.remove(word)
# print(", ".join(word_list))

# #在读取json时检查是否有 's 之类的单词，如果有，就把 's 换成 ’s
# # 读取json文件
# import json
# with open("database/data.json") as f:
#     data = json.load(f)
# # 替换
# '''
# {
#         "word": "apple",
#         "correct": "A round fruit with seeds.'s",
#         "incorrect": [
#           "A type of bird.",
#           "An underwater creature.",
#           "A mode of transportation."
#         ],
#         "example": "I enjoy eating a juicy apple for breakfast."
#       },
# '''
# def replace_s(word):
#     if "'s" in word["correct"]:
#         word["correct"] = word["correct"].replace("'s", "’s")
#     for i in range(len(word["incorrect"])):
#         if "'s" in word["incorrect"][i]:
#             word["incorrect"][i] = word["incorrect"][i].replace("'s", "’s")
#     if "'s" in word["example"]:
#         word["example"] = word["example"].replace("'s", "’s")
#     return word

# word_tuple =  tuple(data)
# for word in data:
#     if "'s" in word["correct"]:
#         word["correct"] = word["correct"].replace("'s", "’s")
#     for i in range(len(word["incorrect"])):
#         if "'s" in word["incorrect"][i]:
#             word["incorrect"][i] = word["incorrect"][i].replace("'s", "’s")
#     if "'s" in word["example"]:
#         word["example"] = word["example"].replace("'s", "’s")
# word_tuple =  tuple(data)
# print(word_tuple)