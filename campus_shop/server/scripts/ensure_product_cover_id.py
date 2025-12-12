import pymysql

def ensure(host: str = '127.0.0.1', user: str = 'root', password: str = 'lzylzy123', database: str = 'campus_shop'):
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW COLUMNS FROM product LIKE 'cover_image_id'")
            exists = cur.fetchone()
            if not exists:
                cur.execute("ALTER TABLE product ADD COLUMN cover_image_id INT NULL AFTER is_reserved")
                conn.commit()
                print('Added column cover_image_id to product')
            cur.execute(
                "UPDATE product p SET p.cover_image_id = (SELECT pi.image_id FROM product_image pi WHERE pi.product_id = p.product_id ORDER BY pi.sort_order LIMIT 1) WHERE p.cover_image_id IS NULL"
            )
            conn.commit()
            print(f'Updated rows: {cur.rowcount}')
            cur.execute("SELECT product_id, cover_image_id FROM product ORDER BY product_id LIMIT 20")
            rows = cur.fetchall()
            for r in rows:
                print({'product_id': r[0], 'cover_image_id': r[1]})
    finally:
        conn.close()

if __name__ == '__main__':
    ensure()

