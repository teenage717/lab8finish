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
    adapter = SQLiteAdapter('shoes_data.db')
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

if __name__ == '__main__':
    main()