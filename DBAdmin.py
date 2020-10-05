import sqlite3


class DB:
    # Конструктор класса бд, создает таблицу, если не существует
    def __init__(self):
        self.conn = sqlite3.connect('store.db')
        self.cursor = self.conn.cursor()

        # self.cursor.execute( '''DROP TABLE IF EXISTS store''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS store (user_id integer , balance integer )''')
        self.conn.commit()

    # Добавление юзера
    def insert_data(self, user_id, balance):
        self.cursor.execute('''INSERT INTO store(user_id, balance) VALUES (?,?)''',
                            (user_id, balance))
        self.conn.commit()


# Класс, с помощью которого можно представить элементы бд в виде объектов
class UserInfo:
    def __init__(self, id, balance):
        self.__id = id
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def get_id(self):
        return self.__id


# Класс для манипуляции данными из бд
class DBHelper:
    def __init__(self, db):
        self.__db = db
        self.users_list = []
        self.__db.cursor.execute("SELECT user_id, balance FROM store")
        self.table = self.__db.cursor.fetchall()
        for element in self.table:
            self.users_list.append(UserInfo(element[0], element[1]))

    # Получить и вывести информацию о юзерах (для отладки)
    def print_user_info(self):
        i = 0
        for i in range(len(self.users_list)):
            print(self.users_list[i].get_id(), self.users_list[i].get_balance())

    # Получить таблицу
    def get_db(self):
        return self.__db

    # Находит юзера по id, если id не существует, создет такого юзера
    def add_user_if_not_exists(self, id):
        exists = False

        i = 0
        for i in range(len(self.users_list)):
            if (self.users_list[i].get_id() == id):
                exists = True
        if (not exists):
            self.__db.insert_data(id, 0)

    # Получить СУЩЕСТВУЮЩЕГО юзера по id
    def find_user_by_id(self, id):
        i = 0
        for i in range(len(self.users_list)):
            if (self.users_list[i].get_id() == id):
                return self.users_list[i]

    #############ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ #################
    # Основной класс для работы с бд - DBHelper


if __name__ == '__main__':
    db = DB()  # Создать экземпляр класса DB
    helper = DBHelper(db)  # Передать конструктору класса DBHelper

    # Добавлять элементы в таблицу : получаем таблицу из DBHelper'a вызовом геттера get_db
    # Заносим информацию методом insert_data(id, баланс)
    helper.get_db().insert_data(1, 2000)
    helper.get_db().insert_data(2, 2321)
    helper.get_db().insert_data(4, 340)

    # С помощью метода find_user_by_id класса DBHelper можно получить юзера по переданному id
    print("FIRST", helper.find_user_by_id(1).get_balance())

    # Метод add_user_if_not_exists добавит в таблицу юзера с  балансом 0, если юзера с таким id нет
    helper.add_user_if_not_exists(3)

    # Баланс любого юзера можно получить, вызвав у него метод get_balance
    print("THIRD", helper.find_user_by_id(3).get_balance())
