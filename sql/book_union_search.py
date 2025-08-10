import MySQLdb
import re
from typing import Union
import book_env

# 引数は検索ワード
# 戻り値はSQLの結果をタプルで返す。
def book_search(words:Union[str, list]) ->tuple:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
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
        col_book = 'book_table.id, book_table.title , book_table.rubi as btr, book_table.writer, book_table.publisher, book_table.memo , book_table.disposal'
        col_writer = 'writer_table.writer, writer_table.rubi'
        col_publisher = 'publisher_table.publisher'
        # テーブル（外部結合）
        tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
        #SQL
        sql = f"SELECT {col_book},{col_writer},{col_publisher} FROM {tables} WHERE {keyword}"
        # del_book_tableのSQL(削除テーブル・著者テーブル・出版社テーブル)
        col_book_d = 'disp_table.id, disp_table.title , disp_table.rubi, disp_table.writer, disp_table.publisher, disp_table.memo , disp_table.disposal'
        col_writer_d = 'writer_table.writer, writer_table.rubi'
        col_publisher_d = 'publisher_table.publisher'
        tables_d ='disp_table LEFT JOIN writer_table ON disp_table.writer = writer_table.id LEFT JOIN publisher_table ON disp_table.publisher = publisher_table.id'
        sql_d = f"SELECT {col_book_d},{col_writer_d},{col_publisher_d} FROM {tables_d} WHERE {keyword1}"
        # タイトルのフリガナ昇順にする
        sorted = 'btr ASC'
        # 書籍テーブルと削除テーブルを結合して表示
        sql_union = f"{sql} UNION ALL {sql_d} ORDER BY {sorted} limit 0,50"
        # ORDER BY（並び替え、デフォルトＩＤ降順）
        cur.execute(sql_union)
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    # ワードが一つの場合どうするか
    input_text = '鈴木 戦国'
    words = ''
    # 入力したキーワードに空白があるか判定
    if re.match(r'^.*\s.*$', input_text):
        # スペース区切りでリストにとる  
        words = input_text.split()
    else:
        # 単独キーワードの場合
        words = input_text    
    result = book_search(words)
    # テスト用にタイトルと著者を表示（10件）
    count=0
    for i,data in enumerate(result):
        print(data[1],data[7],data[6])
        count=i+1
    print(count,'件')
