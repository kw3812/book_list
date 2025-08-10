import MySQLdb
import book_env

# 引数はソート用テキストと読書状態を示すテキストで、戻り値はSQLの結果をタプルで返す。
def book_list(sort:str,state:str) ->tuple:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        # テーブルのカラム
        col_book = 'book_table.id, book_table.title, book_table.rubi, book_table.writer, book_table.publisher, book_table.memo, book_table.state'
        col_writer = 'writer_table.writer, writer_table.rubi as w_rubi'
        col_publisher = 'publisher_table.publisher'
        # テーブル（外部結合）
        tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
        # WHERE句の条件分岐（全て/未読/読書中/既読）
        if state != '全て':
            WHERE = f"WHERE book_table.state = '{state}'"
        else:
            WHERE = "WHERE 1=1" # 全件表示
        # ORDER BY（並び替え、デフォルトＩＤ降順）
        match sort:
            case 'タイトル昇順':
                sorted = 'book_table.rubi ASC'
            case 'タイトル降順':
                sorted = 'book_table.rubi DESC'
            case '著者昇順':
                sorted = 'w_rubi ASC'
            case '著者降順':
                sorted = 'w_rubi DESC'
            case 'ID昇順':
                sorted = 'book_table.id ASC'
            case _:
                sorted = 'book_table.id DESC'
        # SQL    
        sql = f"SELECT {col_book},{col_writer},{col_publisher} FROM {tables} {WHERE} ORDER BY {sorted} limit 0,10"
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    sort = 'タイトル昇順'
    state = '既読' 
    result = book_list(sort,state)
    # テスト用にタイトルと著者を表示（10件）
    count=0
    for i,data in enumerate(result):
        print(data[1],data[7])
        count=i+1
    print(count,'件')
