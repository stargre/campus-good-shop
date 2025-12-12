import pymysql

def add_columns(host: str = '127.0.0.1', user: str = 'root', password: str = 'lzylzy123', database: str = 'campus_shop'):
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW COLUMNS FROM product LIKE 'cover_image_id'")
            exists_id = cur.fetchone()
            if not exists_id:
                cur.execute("ALTER TABLE product ADD COLUMN cover_image_id INT NULL AFTER is_reserved")
                conn.commit()
                print('Added column cover_image_id to product')

            cur.execute("SHOW COLUMNS FROM product LIKE 'cover_image_url'")
            exists_url = cur.fetchone()
            if not exists_url:
                cur.execute("ALTER TABLE product ADD COLUMN cover_image_url VARCHAR(255) NULL AFTER cover_image_id")
                conn.commit()
                print('Added column cover_image_url to product')
    finally:
        conn.close()

if __name__ == '__main__':
    add_columns()

