# Database class to handle MySQL operations
import mysql.connector


class Database():
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            port = '3306',
            user='admin',
            password='root',
            database='fev_employees'
        )
        self.cursor = self.connection.cursor()
        
    def insert_user(self, user_id, first_name, last_name, company, manager_id):
        sql = f'INSERT INTO employees VALUES (%s ,%s, %s, %s, %s);'
        values = (user_id, first_name, last_name, company, manager_id)
        self.cursor.execute(sql, values)
        self.connection.commit()

    def insert_access_record(self, user_id, date, gate_id, direction):
        sql = f'INSERT INTO access VALUES (%s, %s, %s, %s);'
        values = (user_id, date, gate_id, direction)
        self.cursor.execute(sql, values)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

