import MySQLdb
import book_env

# 引数は、タイトル・フリガナ・著者ID・出版社ID・メモ・状態（テキスト）、ID（数値）
# 戻り値はなし
def book_update(title:str,rubi:str,writer:int,publisher:int,memo:str,state:str,id:int):
    # mysqlに接続
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        # ＳＱＬ　
        #sql = "INSERT INTO book_table(title,rubi,writer,publisher,memo) VALUES(title,rubi,writer,publisher,memo)"
        sql = "UPDATE book_table SET title=%s,rubi=%s,writer=%s,publisher=%s,memo=%s,state=%s WHERE id = %s "
        val = (title,rubi,writer,publisher,memo,state,id)
        cur.execute(sql, val)

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    else:
        conn.commit()    
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    id = 14
    title = '鎌倉観光'
    rubi = 'カマクラ'
    writer = 11
    publisher = 10
    memo = '鎌倉のお寺ガイド。'
    state = 'yet'
 
    result = book_update(title,rubi,writer,publisher,memo,state,id)
