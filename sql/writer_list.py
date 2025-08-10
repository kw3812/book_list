import MySQLdb
import book_env

def select_writer():
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        sql = "SELECT * FROM writer_table ORDER BY rubi ASC limit 0,10"
        # sql = "SELECT * FROM writer_table ORDER BY rubi ASC "
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    result = select_writer()
    for x in result:
        print(x)


    
