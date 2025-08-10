import MySQLdb
import book_env

# book_tableにデータを挿入
# 引数にタイトル・フリガナ・著者ID・出版社ID・メモをとる。
def book_insert(title:str,rubi:str,writer:int,publisher:int,memo:str):
    # mysqlに接続
    try:
        #url = 'mysql+pymysql://root:@localhost/book_list?charset=utf8'
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        # ＳＱＬ　
        #sql = "INSERT INTO book_table(title,rubi,writer,publisher,memo) VALUES(title,rubi,writer,publisher,memo)"
        sql = "INSERT INTO book_table(title,rubi,writer,publisher,memo) VALUES(%s, %s, %s, %s, %s)"
        val = (title,rubi,writer,publisher,memo)
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

    title = '日光国立公園'
    rubi = 'ニッコウ'
    writer = 8
    publisher = 5
    memo = '日光の観光と交通。'

    book_insert(title,rubi,writer,publisher,memo)
