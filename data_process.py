import sqlite3
from exception import UserAlreadyExistsError
import uuid
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            image TEXT NOT NULL UNIQUE,
            status 
            origin_text TEXT NOT NULL UNIQUE,
            change_text INTEGER NOT NULL DEFAULT 15,
            update_time DATETIME DEFAULT CURRENT_TIMESTAMP
            bbox
        )
        ''')
        self.conn.commit()

    def create_user(self, wechat_id, verification_code):
        self.cursor.execute('SELECT * FROM users WHERE wechat_id = ? OR verification_code = ?', 
                        (wechat_id, verification_code))
        if self.cursor.fetchone() is not None:
            raise UserAlreadyExistsError("该用户已存在")

        self.cursor.execute('INSERT INTO users (wechat_id, verification_code) VALUES (?, ?)', (wechat_id, verification_code))
        self.conn.commit()

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def get_user_info_by_wechat_id(self, wechat_id):
        self.cursor.execute('SELECT * FROM users WHERE wechat_id = ?', (wechat_id,))
        return self.cursor.fetchone()

    def get_user_info_by_verification_code(self, verification_code):
        self.cursor.execute('SELECT * FROM users WHERE verification_code = ?', (verification_code,))
        return self.cursor.fetchone()  # 返回匹配的用户信息

    def reduce_usage_count(self, verification_code):
        self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
        current_count = self.cursor.fetchone()
        # print(current_count)
        if current_count and current_count[0] > 0:
            self.cursor.execute('UPDATE users SET usage_count = usage_count - 1 WHERE verification_code = ?', (verification_code,))
            self.conn.commit()
        return current_count[0] - 1
    
    def increase_usage_count(self, verification_code, number):
        self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
        current_count = self.cursor.fetchone()
        
        if current_count is not None:
            new_count = current_count[0] + number
            self.cursor.execute('UPDATE users SET usage_count = ? WHERE verification_code = ?', (new_count, verification_code))
            self.conn.commit()

    def increase_usage_count_by_verification_code(self, verification_code, number):
        self.cursor.execute('UPDATE users SET usage_count = usage_count + ? WHERE verification_code = ?', (number, verification_code))
        self.conn.commit()

    def delete_user(self, wechat_id):
        self.cursor.execute("DELETE FROM users WHERE wechat_id = ?", (wechat_id,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
