import psycopg2
from psycopg2 import Error


def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(host='', # Адрес хоста
                                database='',# Имя БД
                                user='',# Имя пользователя
                                password='')# Пароль
        
        print('Connection create')
        return conn
    except Error as err:
        print(f'Connection error\n\n{err}')

def create_tables(conn):
    try:
        with conn.cursor() as cur: 
                cur.execute("""
                DROP TABLE clients_phones;
                DROP TABLE clients;
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS clients(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(30) NOT NULL,
                    surname VARCHAR(30) NOT NULL,
                    email VARCHAR(30) UNIQUE NOT NULL
                    );
                    """)
                
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS clients_phones(
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES clients(id),
                    phone_number VARCHAR(30) NOT NULL
                    );
                """)
                conn.commit()
                print('Tables created')
    except Error as err:
        print(f"Error create tables {err}")

def add_client(conn, name:str, surname:str, email:str,phone:str=None):
    try:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO clients(name, surname, email)
            VALUES (%s, %s, %s) RETURNING id;
            """, (str(name), str(surname), str(email)))

            res = cur.fetchone()

            if phone:
                cur.execute("""
                INSERT INTO clients_phones(client_id, phone_number)
                VALUES (%s, %s);
                """, (res[0], phone))

                conn.commit()

            print(f'Клиент добавлен с ID {res[0]}')
    except Error as err:
        print(f'Ошибка добавления нового клиента\n\n{err}')
    finally:
        conn.close()

def add_phone(conn, client_id:int, phone:str):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO clients_phones(client_id, phone_number)
                VALUES (%s, %s);
                """, (client_id, phone))

            conn.commit()

            print(f'Добавлен номер телефона клиенту {client_id}')
    except Error as err:
        print(f'Ошибка добавления нового клиента\n\n{err}')
    finally:
        conn.close()


def change_client(conn, client_id:int, name: str = None, surname: str = None, email: str = None):
    try:
        with conn.cursor() as cur:
            if name:
                cur.execute("""
                UPDATE clients SET name = %s WHERE id = %s;
                """,(name, client_id))
            if surname:
                cur.execute("""
                UPDATE clients SET surname = %s WHERE id = %s;
                """,(surname, client_id))
            if email:
                cur.execute("""
                UPDATE clients SET email = %s WHERE id = %s;
                """,(email, client_id))
            conn.commit()
            print("Изменения внесены успешно")
    except Error as err:
        print(f'Ошибка изменения данных клиента\n\n{err}')
    finally:
        conn.close()

def del_phone(conn, client_id:int, phone:str):
    try:
        with conn.cursor() as cur:
            cur.exexute("""
            SELECT * FROM clients_phones WHERE client_id =%s;
            """,(client_id,))
            res = cur.fetchall()
            if phone in res:
                cur.execute("""
                DELETE FROM clients_phones WHERE client_id = %s AND phone_number = %s;
                """, (client_id, phone))
                conn.commit()
                print(f"Телефон {phone} успешно удален")
            else:
                print(f"Номер {phone} не найден")
    except Error as err:
        print(f"Ошибка при удалении телефона {err}")
    finally:
        conn.close()

def del_client(conn, client_id):
    try:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM clients_phones WHERE client_id = %s;
            """, (client_id,))
            conn.commit()
            cur.execute("""
            DELETE FROM clients WHERE id = %s;
            """, (client_id,))
            conn.commit()
            print(f"Клиент {client_id} успешно удален")
    except Error as err:
        print(f"Ошибка при удалении клиента {err}")
    finally:
        conn.close()

def show_client(conn, name: str = None, surname: str = None, email: str = None, phone:str = None):
    try:
        with conn.cursor() as cur:
            if name:
                cur.execute("""
                SELECT * FROM clients WHERE name = %s;
                """,(name,))
                result = cur.fetchone()
            if surname:
                cur.execute("""
                SELECT * FROM clients WHERE surname = %s;
                """,(surname,))
                result = cur.fetchone()
            if email:
                cur.execute("""
                SELECT * FROM clients WHERE email = %s;
                """,(email,))
                result = cur.fetchone()
            if phone:
                cur.execute("""
                SELECT client_id FROM clients_phones WHERE phone_number = %s;
                """, (phone,))

                res = cur.fetchone()

                cur.execute("""
                SELECT * FROM clients WHERE id = %s;
                """, (res[0],))
                result = cur.fetchone()
        
            print(f"Клиент: {result}")
    except Error as err:
        print(f'Ошибка \n\n{err}')
    finally:
        conn.close()

#################################################################################################
#Демонстрация
#################################################################################################


# create_tables(create_connection())
# add_client(create_connection(), 'testname', 'testsurname', 'test@email.com', '1234456789')
# add_phone(create_connection(), 1, '987654321')
# change_client(create_connection(), 1, "Test1", 'test2', 'test3')
# del_phone(create_connection(), 1, '1234456789')
# del_client(create_connection(), 1)
# show_client(create_connection(), 'testname')

