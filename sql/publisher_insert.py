import MySQLdb
import book_env

def publisher_insert(publisher:str,rubi:str,memo:str):
    # mysqlに接続
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        sql = "INSERT INTO publisher_table(publisher,rubi,memo) VALUES(%s, %s, %s)"
        val = (publisher,rubi,memo)
        cur.execute(sql, val)
    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    else:
        conn.commit()    
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    publisher = '足立出版'
    rubi = 'アダチシュッパン'
    memo = 'インサートテスト'

    publisher_insert(publisher,rubi,memo)
