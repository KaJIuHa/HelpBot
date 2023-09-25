import psycopg2
from psycopg2 import Error
from create_bot import DB_IP, DB_NAME, DB_PASS, DB_PORT, DB_USER


class Database:
    def __init__(self):
        try:
            # Connect to an existing database
            self.connect = psycopg2.connect(user=DB_USER,
                                            password=DB_PASS,
                                            host=DB_IP,
                                            port=DB_PORT,
                                            database=DB_NAME)

            self.cursor = self.connect.cursor()
            if self.connect:
                print('Data base connected OK')
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
            self.connect.close()

    def check_user(self, user_id):
        """Проверяем пользователя на наличиее"""
        try:
            self.cursor.execute('SELECT * FROM users2 WHERE user_id = %s', (user_id,))
            return bool(self.cursor.fetchone())
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"create_user"}')
            self.connect.rollback()

    def create_user(self, user_id, user_name):
        """Добавление пользователя в БД"""
        try:
            self.cursor.execute('INSERT INTO users2 (user_id,user_name) VALUES (%s,%s)', (user_id, user_name))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"create_user"}')
            self.connect.rollback()

    def check_referal(self, user_id):
        """Проверяем пользователя на наличиее в рефералов"""
        self.cursor.execute('SELECT * FROM referals WHERE tg_id = %s', (user_id,))
        return bool(self.cursor.fetchone())

    def create_referal(self, user_id, referer_id):
        """Добавление пользователя в БД"""
        try:
            self.cursor.execute('INSERT INTO referals (tg_id,referer_id) VALUES (%s,%s)', (user_id, referer_id))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"create_referal"}')
            self.connect.rollback()

    def get_referal(self, user_id):
        """Проверяем пользователя на наличиее в рефералов"""
        self.cursor.execute('SELECT * FROM referals WHERE referer_id = %s', (user_id,))
        return len(self.cursor.fetchall())

    def get_user(self, user_id):
        """Проверяем пользователя данные пользователя"""
        self.cursor.execute('SELECT balance,referals FROM users2 WHERE user_id = %s', (user_id,))
        return self.cursor.fetchone()

    def get_username(self, user_id):
        """Получаем имя пользователя"""
        self.cursor.execute('SELECT user_name FROM users2 WHERE user_id = %s', (user_id,))
        return self.cursor.fetchone()

    def get_user_mark(self, user_id):
        """Проверяем пользователя данные пользователя"""
        self.cursor.execute('SELECT mark FROM users2 WHERE user_id = %s', (user_id,))
        return self.cursor.fetchone()

    def get_game(self):
        self.cursor.execute('SELECT * FROM games')
        return self.cursor.fetchall()

    def get_categories(self, idx):
        self.cursor.execute('SELECT id,title FROM categories WHERE game_id = %s', (idx,))
        return self.cursor.fetchall()

    def get_user_info(self, user_id):
        """Проверяем пользователя данные пользователя"""
        self.cursor.execute('SELECT balance,mark FROM users2 WHERE user_id = %s', (user_id,))
        return self.cursor.fetchone()

    def get_ref(self, user_id):
        """Получаем id реферала"""
        self.cursor.execute('SELECT referer_id FROM referals WHERE tg_id = %s', (user_id,))
        return self.cursor.fetchone()

    def update_user_balance(self, user_id, money):
        """Обновляем статус пользователя"""
        try:
            self.cursor.execute('UPDATE users2 SET balance = balance + %s WHERE user_id = %s', (money, user_id))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_user_status"}')
            self.connect.rollback()

    def check_user_balance(self, user_id):
        """Проверяем баланс пользователя"""
        try:
            self.cursor.execute("""SELECT balance FROM users2 WHERE user_id = %s""", (user_id,))
            return self.cursor.fetchone()[0]
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"check_user_balance"}')
            self.connect.rollback()

    def update_user_balance_money(self, data):
        """Обновляем баланс пользователя в блоке рассылки"""
        try:
            self.cursor.execute(f"""UPDATE users2 SET balance = balance - %s 
            WHERE user_id = %s""", (data['value'], data['user_id']))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_user_balance_money"}')
            self.connect.rollback()

    def get_prop_list_active(self, user_id):
        """Проверяем баланс пользователя"""
        try:
            self.cursor.execute("""SELECT title,id FROM propositions WHERE user_id = %s AND is_on = 1""", (user_id,))
            return self.cursor.fetchall()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_prop_list_active"}')
            self.connect.rollback()

    def get_prop_list_deactive(self, user_id):
        """Проверяем баланс пользователя"""
        try:
            self.cursor.execute("""SELECT title,id FROM propositions WHERE user_id = %s AND is_on = 0""", (user_id,))
            return self.cursor.fetchall()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_prop_list_deactive"}')
            self.connect.rollback()

    def get_prop_list_all(self, user_id):
        """Проверяем баланс пользователя"""
        try:
            self.cursor.execute("""SELECT title,id FROM propositions WHERE user_id = %s""", (user_id,))
            return self.cursor.fetchall()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_prop_list_all"}')
            self.connect.rollback()

    def get_prop_info(self, idx):
        try:
            self.cursor.execute("""SELECT * FROM propositions WHERE id = %s""", (idx,))
            return self.cursor.fetchone()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_prop_info"}')
            self.connect.rollback()

    def get_prop_list(self, idx):
        try:
            self.cursor.execute("""SELECT id,title,price_per_hour FROM propositions WHERE category_id = %s""", (idx,))
            return self.cursor.fetchall()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_prop_list"}')
            self.connect.rollback()

    def get_prop_info_search(self, idx):
        try:
            self.cursor.execute("""SELECT * FROM propositions WHERE category_id = %s""", (idx,))
            return self.cursor.fetchone()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_prop_info_search"}')
            self.connect.rollback()

    def create_par(self, user_id, exe_id):
        """Добавление пользователя в БД"""
        try:
            self.cursor.execute('INSERT INTO execution (user_id,exe_id) VALUES (%s,%s)', (user_id, exe_id))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"create_par"}')
            self.connect.rollback()

    def par_id(self,user_id,exe_id):
        try:
            self.cursor.execute("""SELECT id FROM execution WHERE user_id = %s AND exe_id = %s""", (user_id,exe_id))
            return self.cursor.fetchone()[0]
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"par_id"}')
            self.connect.rollback()

    def update_balance_user(self, user_id,value):
        """Обновляем баланс пользователя в блоке рассылки"""
        try:
            self.cursor.execute(f"""UPDATE users2 SET balance = balance - %s 
            WHERE user_id = %s""", (value, user_id))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_user_balance"}')
            self.connect.rollback()
    def del_apr(self,value):
        """Обновляем баланс пользователя в блоке рассылки"""
        try:
            self.cursor.execute(f"""DELETE  FROM execution WHERE id = %s""", (value,))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"del_apr"}')
            self.connect.rollback()

    def create_prop_in(self,data):
        try:
            self.cursor.execute('INSERT INTO propositions '
                                '(title,price,hours,description,price_per_hour,user_id,user_name,category_id) '
                                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                                (data['title'],
                                data['price'],
                                data['hour'],
                                data['description'],
                                data['price_per_hour'],
                                data['user_id'],
                                data['username'],
                                data['category_id']))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"create_prop"}')
            self.connect.rollback()

    def get_mark(self,user_id):
        try:
            self.cursor.execute('SELECT mark FROM users2 WHERE user_id = %s', (user_id,))
            return self.cursor.fetchone()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"get_mark"}')
            self.connect.rollback()

    def update_user_mark(self, user_id, mark):
        """Обновляем статус пользователя"""
        try:
            self.cursor.execute('UPDATE users2 SET mark = %s WHERE user_id = %s', (mark, user_id))
            self.connect.commit()
        except Exception as ex:
            print(f'Ошибка: {ex}, в функции :{"update_user_status"}')
            self.connect.rollback()
db = Database()
