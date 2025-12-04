from typing import Union
from dbc_abc import BookData

class UnionTable(BookData):

    '''廃棄含む書籍リスト
    引数は、並び替え、表示件数（文字列）
    戻り値は、ＳＱＬの結果と総件数（タプル、タプル）
    '''        
    def list(self,sorted) ->tuple:
        match sorted:
            case 'タイトル昇順':
                sorted = 'btr ASC'
            case 'タイトル降順':
                sorted = 'btr DESC'
            case '著者昇順':
                sorted = 'r_rubi ASC'
            case '著者降順':
                sorted = 'r_rubi DESC'
            case 'ＩＤ昇順':
                sorted = 'id ASC'
            case _:
                sorted = 'id DESC'
        # book_tableのSQL
        # テーブルのカラム（書籍テーブル・著者テーブル・出版社テーブル）
        col_book = 'book_table.id, book_table.title, book_table.rubi , book_table.writer, book_table.publisher, book_table.memo, book_table.disposal, book_table.create_time'
        col_writer = 'writer_table.writer, writer_table.rubi as r_rubi'
        col_publisher = 'publisher_table.publisher'
        # テーブル（外部結合）
        tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
        #SQL  SQL_CALC_FOUND_ROWS
        sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book},{col_writer},{col_publisher} FROM {tables} "
        # del_book_tableのSQL(削除テーブル・著者テーブル・出版社テーブル)
        col_book_d = 'disp_table.id, disp_table.title, disp_table.rubi, disp_table.writer, disp_table.publisher, disp_table.memo, disp_table.disposal, disp_table.create_time'
        # col_writer_d = 'writer_table.writer, writer_table.rubi as r_rubi'
        # col_publisher_d = 'publisher_table.publisher'
        tables_d ='disp_table LEFT JOIN writer_table ON disp_table.writer = writer_table.id LEFT JOIN publisher_table ON disp_table.publisher = publisher_table.id'
        sql_d = f"SELECT {col_book_d},{col_writer},{col_publisher} FROM {tables_d} "
        # 書籍テーブルと削除テーブルを結合して表示 limit 0,100
        # sql_union = f"{sql} UNION ALL {sql_d} ORDER BY {sorted} LIMIT {limit}"
        sql_union = f"{sql} UNION ALL {sql_d} ORDER BY {sorted} "
        count = "SELECT FOUND_ROWS()"
        # ORDER BY（並び替え、デフォルトＩＤ降順）
        try:
            with self.cursor() as cur:
                cur.execute(sql_union)
                result = cur.fetchall()
                cur.execute(count)
                count_all = cur.fetchone()
                return result, count_all

        except Exception as e:
            print('データベースの接続に失敗しました。',e)

    '''廃棄含む書籍検索（スペース区切りで２つまで）
    引数は、検索ワード（文字列orリスト）
    戻り値は、ＳＱＬの結果と総件数（タプル、タプル）
    '''        
    def search(self,words:Union[str, list]) ->tuple:
        # キーワード用の変数       
        word = words[0]
        word1 = words[1]
        keyword = ''
        keyword1 =''
        # キーワードの数でＳＱＬを差し替える
        if len(words) == 2:
            # キーワード２つでタイトルとメモと著者から検索（word,word1）
            keyword = f"(book_table.title LIKE '%{word}%' OR book_table.memo LIKE '%{word}%' OR writer_table.writer LIKE '%{word}%') AND (book_table.title LIKE '%{word1}%' OR book_table.memo LIKE '%{word1}%'  OR writer_table.writer LIKE '%{word1}%')"
            keyword1 = f"(disp_table.title LIKE '%{word}%' OR disp_table.memo LIKE '%{word}%' OR writer_table.writer LIKE '%{word}%') AND (disp_table.title LIKE '%{word1}%' OR disp_table.memo LIKE '%{word1}%'  OR writer_table.writer LIKE '%{word1}%')"
        else:
            # キーワード一つでタイトルとメモと著者から検索（words）
            keyword = f"book_table.title LIKE '%{words}%' OR book_table.memo LIKE '%{words}%' OR writer_table.writer LIKE '%{words}%'"
            keyword1 = f"disp_table.title LIKE '%{words}%' OR disp_table.memo LIKE '%{words}%' OR writer_table.writer LIKE '%{words}%'"
        # book_tableのSQL
        # テーブルのカラム（書籍テーブル・著者テーブル・出版社テーブル）
        col_book = 'book_table.id, book_table.title , book_table.rubi as btr, book_table.writer, book_table.publisher, book_table.memo , book_table.disposal, book_table.create_time'
        col_writer = 'writer_table.writer, writer_table.rubi as r_rubi'
        col_publisher = 'publisher_table.publisher'
        # テーブル（外部結合）
        tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
        #SQL
        sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book},{col_writer},{col_publisher} FROM {tables} WHERE {keyword}"
        # del_book_tableのSQL(削除テーブル・著者テーブル・出版社テーブル)
        col_book_d = 'disp_table.id, disp_table.title , disp_table.rubi, disp_table.writer, disp_table.publisher, disp_table.memo , disp_table.disposal, disp_table.create_time'
        # col_writer_d = 'writer_table.writer, writer_table.rubi'
        # col_publisher_d = 'publisher_table.publisher'
        tables_d ='disp_table LEFT JOIN writer_table ON disp_table.writer = writer_table.id LEFT JOIN publisher_table ON disp_table.publisher = publisher_table.id'
        sql_d = f"SELECT {col_book_d},{col_writer},{col_publisher} FROM {tables_d} WHERE {keyword1}"
        # 書籍テーブルと削除テーブルを結合して表示 limit 0,50
        # sql_union = f"{sql} UNION ALL {sql_d} ORDER BY {sorted} LIMIT {limit} "
        sql_union = f"{sql} UNION ALL {sql_d} ORDER BY id DESC "
        count = "SELECT FOUND_ROWS()"
        try:
            with self.cursor() as cur:
                cur.execute(sql_union)
                result = cur.fetchall()
                cur.execute(count)
                count_all = cur.fetchone()
                return result, count_all

        except Exception as e:
            print('データベースの接続に失敗しました。',e)

    def detail(self):
        pass
    def insert(self):
        pass
    def update(self):
        pass
    def delete(self):
        pass
    
if __name__ == '__main__':
    sorted = 'id DESC'
    words = '戦国'
    union = UnionTable(sorted)
    result = union.search(words)
    # テスト用にタイトルと著者を表示（10件）
    print(result)
