import MySQLdb
import book_env

def publisher_delete(id:int):
    # mysqlに接続
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        # ＳＱＬ　
        sql = "DELETE FROM publisher_table WHERE id = %s "
        # データはタプルにする必要がある（ , を付けるとタプルに）
        cur.execute(sql, (id,))

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    else:
        conn.commit()    
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    id = 133
 
    result = publisher_delete(id)
