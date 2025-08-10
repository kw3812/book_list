import MySQLdb
import book_env

def writer_update(writer:str,rubi:str,memo:str,id:int):
    # mysqlに接続
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        # ＳＱＬ　
        sql = "UPDATE writer_table SET writer=%s,rubi=%s,memo=%s WHERE id = %s "
        val = (writer,rubi,memo,id)
        cur.execute(sql, val)

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    else:
        conn.commit()    
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    id = 708
    writer = '会津次郎'
    rubi = 'アイズジロウ'
    memo = 'アップデートテスト'
 
    result = writer_update(writer,rubi,memo,id)
