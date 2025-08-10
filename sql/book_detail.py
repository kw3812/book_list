import MySQLdb
import book_env

# idをキーにしてbook_tableの該当データにアクセス
# 引数のidは数値で、戻り地はSQLの結果をタプルで返す
def book_detail(id:int)->tuple:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        columns = 'book_table.id, book_table.title, book_table.rubi, book_table.writer,writer_table.writer, book_table.publisher, publisher_table.publisher,book_table.memo, book_table.state'
        tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id' 
        sql = f"SELECT {columns} FROM {tables} WHERE book_table.id = {id}"
        cur.execute(sql )
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    id = 11 
    result = book_detail(id)

    print(result)
