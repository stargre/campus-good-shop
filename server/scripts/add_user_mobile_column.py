import pymysql

def add_user_mobile_column(host: str = '127.0.0.1', user: str = 'root', password: str = 'lzylzy123', database: str = 'campus_shop'):
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW COLUMNS FROM user_info LIKE 'user_mobile'")
            exists = cur.fetchone()
            if not exists:
                cur.execute("ALTER TABLE user_info ADD COLUMN user_mobile VARCHAR(20) NULL AFTER user_email")
                conn.commit()
                print('Added column user_mobile to user_info')
            else:
                print('Column user_mobile already exists')
    finally:
        conn.close()

if __name__ == '__main__':
    add_user_mobile_column()

