import MySQLdb
import book_env


# 引数はソート用テキストと読書状態を示すテキストで、戻り値はSQLの結果をタプルで返す。
def book_list(table_name) ->tuple:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        # テーブルのカラム
        col_book = f'{table_name}.id, {table_name}.title, {table_name}.writer, {table_name}.publisher,{table_name}.memo,{table_name}.create_time'
        col_writer = 'writer_table.writer, writer_table.rubi'
        col_publisher = 'publisher_table.publisher'
        # テーブル（外部結合）
        tables = f'{table_name} LEFT JOIN writer_table ON {table_name}.writer = writer_table.id LEFT JOIN publisher_table ON {table_name}.publisher = publisher_table.id'
        sorted = f'{table_name}.id DESC'
        # SQL    
        sql = f"SELECT {col_book},{col_writer},{col_publisher} FROM {tables} ORDER BY {sorted} "
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()
        
# 引数はソート用テキストと読書状態を示すテキストで、戻り値はSQLの結果をタプルで返す。
def book_union() ->tuple:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        # テーブルのカラム
        col_book = 'book_table.id, book_table.title, book_table.writer, book_table.publisher, book_table.disposal'
        col_disp = 'disp_table.id, disp_table.title, disp_table.writer, disp_table.publisher, disp_table.disposal'
        col_writer = 'writer_table.writer, writer_table.rubi'
        col_publisher = 'publisher_table.publisher'
        # テーブル（外部結合）
        table_book = 'book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
        table_disp = 'disp_table LEFT JOIN writer_table ON disp_table.writer = writer_table.id LEFT JOIN publisher_table ON disp_table.publisher = publisher_table.id'
        # sorted = f'{table_name}.id DESC'
        # SQL    
        sql_book = f"SELECT {col_book},{col_writer},{col_publisher} FROM {table_book}"
        sql_disp = f"SELECT {col_disp},{col_writer},{col_publisher} FROM {table_disp} "
        sql_union = f"{sql_book} UNION ALL {sql_disp} ORDER BY id DESC LIMIT 20"

        cur.execute(sql_union)
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':

    result = book_union()
    # テスト用にタイトルと著者を表示（10件）
    for data in result:
        print(data[1],data[4])

