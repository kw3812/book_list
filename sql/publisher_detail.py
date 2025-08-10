import MySQLdb
import book_env

def publisher_detail(id:int)->tuple:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        sql = f"SELECT * FROM publisher_table WHERE id = {id}"
        cur.execute(sql )
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    id = 63 
    result = publisher_detail(id)

    print(result)
