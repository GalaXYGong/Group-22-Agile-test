import pytest
from unittest import mock
from usermod import execute, select, select_id, update, insert, create, select_username, select_all, delete
import usermod
@pytest.fixture
def mock_cursor():
    with mock.patch('usermod.cursor') as mock_cursor:
        yield mock_cursor

@pytest.fixture
def mock_connection():
    with mock.patch('usermod.connection') as mock_connection:
        yield mock_connection

def test_execute(mock_connection, mock_cursor):
    statement = "CREATE TABLE test (id INTEGER)"
    execute(statement)
    mock_cursor.execute.assert_called_once_with(statement)
    mock_connection.commit.assert_called_once()


def test_drop(mock_connection, mock_cursor):
    table_name = "test"
    usermod.drop(table_name)
    mock_cursor.execute.assert_called_once_with(f"DROP TABLE IF EXISTS {table_name.upper()}")
    mock_connection.commit.assert_called_once()


def test_select(mock_cursor):
    table_name = "test"
    column_name = "*"
    expected_result = [(1,), (2,)]
    # 创建一个 MagicMock 对象来模拟 execute 返回的对象
    mock_execute = mock.MagicMock()
    mock_execute.fetchall.return_value = expected_result
    # 设置 mock_cursor.execute 返回这个 MagicMock 对象
    mock_cursor.execute.return_value = mock_execute
    result = usermod.select(table_name, column_name)
    mock_cursor.execute.assert_called_once_with(f"SELECT {column_name} FROM {table_name}")
    assert result == expected_result


def test_select_id(mock_cursor):
        table_name = "test"
        id = 1
        column_name = "*"
        expected_result = (1,)
        mock_execute = mock.MagicMock()
        mock_execute.fetchone.return_value = expected_result
        mock_cursor.execute.return_value = mock_execute
        result = usermod.select_id(table_name, id, column_name)
        mock_cursor.execute.assert_called_once_with(f"SELECT {column_name} FROM {table_name} WHERE id = {id}")
        assert result == expected_result



def test_update(mock_connection, mock_cursor):
    table_name = "test"
    column_name = "name"
    value = "John"
    condition = "id = 1"
    usermod.update(table_name, column_name, value, condition)
    mock_cursor.execute.assert_called_once_with(f"UPDATE {table_name} SET {column_name} = '{value}' WHERE {condition}")
    mock_connection.commit.assert_called_once()


def test_insert(mock_connection, mock_cursor):
    table_name = "test"
    column_name = ["id", "name"]
    value = [(1, "John")]
    usermod.insert(table_name, column_name, value)
    mock_cursor.execute.assert_called_once_with(f"INSERT INTO {table_name}({column_name}) VALUES {value}")
    mock_connection.commit.assert_called_once()


def test_create(mock_connection, mock_cursor):
    table_name = "users"
    column_name = "id, name"
    value = "1, 'John'"
    usermod.create(table_name, column_name, value)
    mock_cursor.execute.assert_called_once_with(f"INSERT INTO {table_name}({column_name}) VALUES ({value})")
    mock_connection.commit.assert_called_once()

def test_select_username():
    with mock.patch('usermod.cursor') as mock_cursor:
        username = "John"
        column_name = "*"
        expected_result = (1, "John")
        mock_execute = mock.MagicMock()
        mock_execute.fetchone.return_value = expected_result
        mock_cursor.execute.return_value = mock_execute
        result = usermod.select_username(username, column_name)
        mock_cursor.execute.assert_called_once_with(f'SELECT {column_name} FROM account WHERE username = "{username}"')
        assert result == expected_result

def test_select_all():
    with mock.patch('usermod.cursor') as mock_cursor:
        table_name = "test"
        column_name = "*"
        expected_result = [(1,), (2,)]
        mock_execute = mock.MagicMock()
        mock_execute.fetchall.return_value = expected_result
        mock_cursor.execute.return_value = mock_execute
        result = usermod.select_all(table_name, column_name)
        mock_cursor.execute.assert_called_once_with(f'SELECT {column_name} FROM {table_name}')
        assert result == expected_result

@mock.patch('usermod.cursor')
def test_delete(mock_cursor):
    table_name = "test"
    condition = "id=1"
    condition_list = condition.split("=")
    real_condition = condition_list[0] + "='" + condition_list[1] + "'"
    usermod.delete(table_name, condition)
    mock_cursor.execute.assert_called_once_with(f"DELETE FROM {table_name} WHERE {real_condition}")

def test_insert_secure_question(mock_connection, mock_cursor):
    username = "xinyu"
    secure_question1 = "What is your favorite color?"
    answer1 = "red"
    secure_question2 = "What is your favorite food?"
    answer2 = "pizza"
    usermod.insert_secure_question(username, secure_question1, answer1, secure_question2, answer2)
    mock_cursor.execute.assert_called_once_with(f"UPDATE ACCOUNT SET secure_question1 = '{secure_question1}:{answer1}', secure_question2 = '{secure_question2}:{answer2}' WHERE username = '{username}'")
