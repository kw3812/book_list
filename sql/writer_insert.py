import MySQLdb
import book_env

def writer_insert(writer:str,rubi:str,memo:str):
    # mysqlに接続
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        sql = "INSERT INTO writer_table(writer,rubi,memo) VALUES(%s, %s, %s)"
        val = (writer,rubi,memo)
        cur.execute(sql, val)
        #cur.fetchall()
    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    else:
        conn.commit()    
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    writer = '会津太郎'
    rubi = 'あいずたろう'
    memo = 'インサートテスト。'

    writer_insert(writer,rubi,memo)
