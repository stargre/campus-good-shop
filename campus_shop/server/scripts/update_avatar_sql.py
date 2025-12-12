import pymysql

def update(host: str = '127.0.0.1', user: str = 'root', password: str = 'lzylzy123', database: str = 'campus_shop'):
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE user_info SET user_avart = '/upload/avatar/1676553050529.png' WHERE user_avart NOT LIKE '/upload/%'")
            conn.commit()
            print('Avatar paths updated:', cur.rowcount)
    finally:
        conn.close()

if __name__ == '__main__':
    update()

