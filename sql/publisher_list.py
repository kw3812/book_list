import MySQLdb
import book_env

def select_publisher():
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        sql = "SELECT * FROM publisher_table ORDER BY rubi ASC"
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    result = select_publisher()
    for x in result:
        print(x)
    #writers = witer_list.select_writer()    
    print([row[1] for row in witer_list.select_writer()])    
