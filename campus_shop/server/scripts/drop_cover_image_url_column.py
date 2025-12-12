import pymysql

def drop_column(host: str = '127.0.0.1', user: str = 'root', password: str = 'lzylzy123', database: str = 'campus_shop'):
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW COLUMNS FROM product LIKE 'cover_image_url'")
            exists = cur.fetchone()
            if exists:
                cur.execute("ALTER TABLE product DROP COLUMN cover_image_url")
                conn.commit()
                print('Dropped column cover_image_url from product')
            else:
                print('Column cover_image_url not found')
    finally:
        conn.close()

if __name__ == '__main__':
    drop_column()

