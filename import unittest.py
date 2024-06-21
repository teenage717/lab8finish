import unittest
from unittest.mock import patch
from io import StringIO
import sqlite3

class SQLiteAdapter:
    def __init__(self, db_file):
        self._connection = None
        self._db_file = db_file

    def connect(self):
        self._connection = sqlite3.connect(self._db_file)

    def disconnect(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute_query(self, query):
        if self._connection:
            cursor = self._connection.cursor()
            cursor.execute(query)
            self._connection.commit()
            return cursor.fetchall()

        return None

def main():
    adapter = SQLiteAdapter(':memory:')
    adapter.connect()

    while True:
        print("1. Выполнить SQL-запрос")
        print("2. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            sql_query = input("Введите SQL-запрос: ")
            result = adapter.execute_query(sql_query)
            print("Результат:")
            for row in result:
                print(row)
        elif choice == '2':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    adapter.disconnect()

class SQLiteAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.adapter = SQLiteAdapter(':memory:')
        self.adapter.connect()

    def tearDown(self):
        self.adapter.disconnect()

    @patch('builtins.input', side_effect=['1', 'SELECT * FROM shoes', '2'])
    def test_execute_query(self, mock_input):
        expected_output = [
            (1, 'Nike', 'Air Max'),
            (2, 'Adidas', 'Superstar'),
            (3, 'Puma', 'Suede')
        ]

        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.adapter.execute_query('CREATE TABLE shoes (id INT, brand TEXT, name TEXT);')
            self.adapter.execute_query('INSERT INTO shoes VALUES (1, "Nike", "Air Max");')
            self.adapter.execute_query('INSERT INTO shoes VALUES (2, "Adidas", "Superstar");')
            self.adapter.execute_query('INSERT INTO shoes VALUES (3, "Puma", "Suede");')
            main()

        output = mock_stdout.getvalue().strip().split('\n')[3:]  # Exclude menu options
        output = [tuple(map(str.strip, line.split(','))) for line in output]

        self.assertEqual(output, expected_output)

    @patch('builtins.input', side_effect=['2'])
    def test_exit_program(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            main()

        output = mock_stdout.getvalue().strip()

        self.assertEqual(output, '1. Выполнить SQL-запрос\n2. Выйти\nВыберите действие:')

if __name__ == '__main__':
    unittest.main()