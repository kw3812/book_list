import MySQLdb
from contextlib import contextmanager
from book_env import USER, PASSWORD, HOST, DB, CHARSET

class Chart():
    def __init__(self):
        self.conn = MySQLdb.connect(user=USER, passwd=PASSWORD, host=HOST, db=DB, charset=CHARSET)
        
    @contextmanager
    def cursor(self):
        """
        カーソルのクローズを with で自動化する。
        失敗時はロールバック、成功時はコミット。
        """
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()

    # 著者別カウントグラフ用の集計
    def writer_count(self):
        # テーブルのカラム
        col_book = 'book_table.id, book_table.writer'
        col_writer = 'writer_table.id, writer_table.writer, count(writer_table.writer) as count_wtriter'
        # テーブル（外部結合）
        tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id '
        # グルーピング
        group = 'writer_table.id'
        # 著者名の「その他」と「不明」は条件からはずす
        etc = 'writer_table.id = 146 OR writer_table.id = 184'
        # 並び替え　著者カウント降順
        sort = 'count_wtriter DESC'
        # SQL    
        sql = f"SELECT {col_book},{col_writer} FROM {tables} WHERE NOT {etc} GROUP BY {group} ORDER BY {sort} limit 0,10"
        try:
            with self.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()
                return result

        except Exception as e:
            print('データベースの接続に失敗しました。',e)

    # 出版社カウントグラフ用の集計
    def publisher_count(self):       
        # テーブルのカラム
        col_book = 'book_table.id, book_table.publisher'
        col_publisher = 'publisher_table.id, publisher_table.publisher, count(publisher_table.publisher) as count_publisher'
        # テーブル（外部結合）
        tables ='book_table LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id '
        # グルーピング
        group = 'publisher_table.id'
        # 出版社名の「不明」は条件からはずす
        etc = 'publisher_table.id = 45'
        # 並び替え　著者カウント降順
        sort = 'count_publisher DESC'
        # SQL    
        sql = f"SELECT {col_book},{col_publisher} FROM {tables} WHERE NOT {etc} GROUP BY {group} ORDER BY {sort} limit 0,10"
        try:
            with self.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()
                return result

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
            
    def all_count(self) -> tuple:
        sql1 = "SELECT count(*) FROM book_table"
        sql2= "SELECT count(*) FROM disp_table"
        sql_union = f"{sql1} UNION ALL {sql2}  "
        try:
            with self.cursor() as cur:
                cur.execute(sql_union )
                result = cur.fetchall()
                return result
        except Exception as e:
            print('データベースの接続に失敗しました。',e)

# if __name__ == '__main__':

#     #result = writer_count()
#     result = publisher_count()
#     print(result)


