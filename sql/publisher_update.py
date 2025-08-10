import MySQLdb
import book_env

def publisher_update(publisher:str,rubi:str,memo:str,id:int):
    # mysqlに接続
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        # ＳＱＬ　
        sql = "UPDATE publisher_table SET publisher=%s,rubi=%s,memo=%s WHERE id = %s "
        val = (publisher,rubi,memo,id)
        cur.execute(sql, val)

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    else:
        conn.commit()    
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    id = 133
    publisher = '足立出版'
    rubi = 'アダチシュッパン'
    memo = 'アップデートテスト'
 
    result = publisher_update(publisher,rubi,memo,id)
