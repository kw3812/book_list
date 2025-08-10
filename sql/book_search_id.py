import MySQLdb
import book_env

conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
# 入力された著者名から著者ＩＤを求める
# 引数はテキストで、戻り値は数値
def search_id_writer(word:str)->int:
    try:
        cur = conn.cursor()
        sql = f"SELECT id, writer FROM writer_table WHERE writer = '{word}'"
        cur.execute(sql )
        result = cur.fetchall()
        return result[0][0]
    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    def seach():
        word = "鈴木光司"
        writer_id = search_id_writer(word)
        print(type(writer_id))
        print(writer_id)
    seach()

# 入力された出版社名から出版社ＩＤを求める
# 引数はテキストで、戻り値は数値
def search_id_publisher(word:str)->int:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        sql = f"SELECT id, publisher FROM publisher_table WHERE publisher = '{word}'"
        cur.execute(sql )
        result = cur.fetchall()
        return result[0][0]
    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    def seach():
        word = "講談社"
        writer_id = search_id_publisher(word)
        print(type(writer_id))
        print(writer_id)
    seach()
