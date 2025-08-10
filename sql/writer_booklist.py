import MySQLdb
import book_env

# 特定の著者の本のリスト
# 引数は数値で、戻り値はタプル
def book_list(id:int)->tuple:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        col_book = 'book_table.id, book_table.title, book_table.writer, book_table.publisher'
        col_writer = 'writer_table.id, writer_table.writer '
        col_publisher = 'publisher_table.id, publisher_table.publisher'
        # テーブル（外部結合）
        tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
        sql = f"SELECT {col_book},{col_writer},{col_publisher} FROM {tables} WHERE book_table.writer = {id}"
        cur.execute(sql )
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    id = 558
    result = book_list(id)
    count=0
    for i,data in enumerate(result):
        print(data[1],data[7])
        count=i+1
    print(count,'件')
    print(type(result))
