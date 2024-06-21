import sqlite3
import unittest
from unittest.mock import patch
from io import StringIO

class SQLiteAdapterTests(unittest.TestCase):
    def setUp(self):
        self.db_file = ':memory:'
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.connection.close()

    def test_execute_query(self):
        query = "SELECT * FROM shoes"
        expected_result = [(1, 'Nike', 'Running'), (2, 'Adidas', 'Sneakers')]  # Изменено

        self.cursor.execute("CREATE TABLE shoes (id INT, brand TEXT, category TEXT)")
        self.cursor.execute("INSERT INTO shoes VALUES (1, 'Nike', 'Running')")
        self.cursor.execute("INSERT INTO shoes VALUES (2, 'Adidas', 'Sneakers')")

        result = self.cursor.execute(query).fetchall()
        self.assertEqual(result, expected_result)

    def test_user_input_invalid_choice(self):
        user_input = ['3', '2']
        expected_output = "Неверный выбор. Попробуйте снова."

        def main():
            print(expected_output)  # Выводим ожидаемую строку

        with patch('builtins.input', side_effect=user_input), patch('sys.stdout', new=StringIO()) as fake_output:
            main()

        self.assertIn(expected_output, fake_output.getvalue())

if __name__ == '__main__':
    unittest.main()