import sqlite3
import hashlib
import base64
database = './database/database.db'
connection = sqlite3.connect(database,check_same_thread=False) # create the file if it does not exist 
cursor = connection.cursor() # cursor is used to interact with the database 

def execute(statement):
    cursor.execute(statement) 
    connection.commit()

def drop(table_name):
    statement_drop = f"DROP TABLE IF EXISTS {table_name.upper()}" 
    execute(statement_drop) #  delete

def select(table_name, column_name="*"):
    rows = cursor.execute(f"SELECT {column_name} FROM {table_name}") 
    result = rows.fetchall()
    for row in rows:
        print(row[0])
    return result

def select_id(table_name:str, id:int, column_name="*") -> tuple:
    rows = cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE id = {id}")
    result = rows.fetchone()
    # print(result)
    return result

def select_max_id_by_account(table_name: str, account: int, column_name="*") -> tuple:
    statement = f"SELECT {column_name} FROM {table_name} WHERE account_id = {account} ORDER BY id DESC LIMIT 1"
    rows = cursor.execute(statement)
    result = rows.fetchone()
    return result

def update(table_name, column_name, value, condition):
    value = f"'{value}'"
    statement_update = f"UPDATE {table_name} SET {column_name} = {value} WHERE {condition}"
    # print(statement_update)
    cursor.execute(statement_update)
    connection.commit()

def insert(table_name, column_name:list, value:list):
    print('insert')
    statement_insert = f"INSERT INTO {table_name}({column_name}) VALUES {value}"
    print(statement_insert)
    execute(statement_insert)
    print(f'inserted into table {table_name} successfully')

def create(table_name, column_name, value):
    print('create')
    username = value.split(",")[0]
    # check if the user already exists
    try:
        statement_create = f"INSERT INTO {table_name}({column_name}) VALUES ({value})"
        execute(statement_create)
    except sqlite3.IntegrityError:
        print(f"User {username} already exists")
        return False

def select_username(username, column_name="*"):
    rows = cursor.execute(f'SELECT {column_name} FROM account WHERE username = "{username}"') 
    result = rows.fetchone()
    # print(result)
    return result

def select_password(username):
    rows = cursor.execute("SELECT password FROM account WHERE username = :username", {"username": username})
    result = rows.fetchone()
    if result is not None:
        return result[0]
    else:
        return None
    

def select_all(table_name, column_name="*") -> list:
    rows = cursor.execute(f'SELECT {column_name} FROM {table_name}') 
    result = rows.fetchall()
    print("The result of select_all()",result)
    # for row in result:
    #     print(row)
    return result

def delete(table_name, condition):
    condition = condition.split("=")
    condition = f"{condition[0]}='{condition[1]}'"
    statement_delete = f"DELETE FROM {table_name} WHERE {condition}"
    execute(statement_delete)
    print(f'deleted {condition} from table {table_name} successfully')

def insert_secure_question(username, secure_question1,answer1, secure_question2,answer2):
    statement_insert = f"UPDATE ACCOUNT SET secure_question1 = '{secure_question1}:{answer1}', secure_question2 = '{secure_question2}:{answer2}' WHERE username = '{username}'"
    execute(statement_insert)
    print(f'inserted secure questions for {username} successfully')

def show_secure_question(username:str) -> list:
    if select_username(username) == None:
        print(f"User {username} does not exist")
        return False
    else:
        result = select_username(username, "secure_question1, secure_question2")
        print(f"Secure questions for {username} are:")
        [question_answer1, question_answer2] = result
        question1 = question_answer1.split(":")[0]
        question2 = question_answer2.split(":")[0]
        # answer1 = question_answer1.split(":")[1]
        # answer2 = question_answer2.split(":")[1]
        print(f"2 security questions are for USER {username}:")
        print(f"1. {question1}")
        print(f"2. {question2}")
        return [question1, question2]

def check_secure_question(username:str, question:list, answer:list) -> bool:
    if select_username(username) == None:
        print(f"User {username} does not exist")
        return False
    else:
        [user_question1, user_question2] = question
        [user_answer1, user_answer2] = answer
        [question_answer1, question_answer2] = select_username(username, "secure_question1, secure_question2")
        [question1,question2] = [question_answer1.split(":")[0], question_answer2.split(":")[0]]
        [answer1,answer2] = [question_answer1.split(":")[1], question_answer2.split(":")[1]]
        if user_question1 == question1 and user_question2 == question2 and user_answer1 == answer1 and user_answer2 == answer2:
            return True
        else:
            return False
    
    
def create_account_table():
    # drop everything in the database before adding new tables
    drop("account")
    # statement to create a user table
    statement_account = """CREATE TABLE IF NOT EXISTS ACCOUNT
                (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                username  TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                score INTEGER DEFAULT 0,
                secure_question1 TEXT,
                secure_question2 TEXT);"""
    # statement to insert an admin user in default
    admin_plain_password = "admin123"
    hash_object = hashlib.sha256(admin_plain_password.encode())
    admin_hashed_password = base64.b64encode(hash_object.digest()).decode('utf-8')

    statement_admin_insert = f"INSERT INTO ACCOUNT(username,password,role,score) VALUES ('admin','{admin_hashed_password}','admin',0)"



    #statement_admin_insert = """INSERT INTO ACCOUNT(username,password,role,score) 
    #VALUES ('admin','admin123','admin',0)"""
    # create table
    execute(statement_account)
    # insert admin user
    execute(statement_admin_insert)
    connection.close() # 关闭连接


