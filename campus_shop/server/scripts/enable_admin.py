import pymysql

def enable_admin(student_id: str = 'admin', host: str = '127.0.0.1', user: str = 'root', password: str = 'lzylzy123', database: str = 'campus_shop'):
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE user_info SET user_status=1, role='1', token=%s WHERE user_student_id=%s", (student_id+'admin', student_id))
            conn.commit()
            cur.execute("SELECT user_id, user_student_id, user_status, role FROM user_info WHERE user_student_id=%s", (student_id,))
            row = cur.fetchone()
            print({
                'user_id': row[0] if row else None,
                'user_student_id': row[1] if row else None,
                'user_status': row[2] if row else None,
                'role': row[3] if row else None,
            })
    finally:
        conn.close()

if __name__ == '__main__':
    enable_admin()
