import MySQLdb
import re
from typing import Union
import book_env

# キーワード検索用のＳＱＬ
# 引数のキーワードは、テキストorリスト
# 戻り地はSQLの結果をタプルで返す
def book_search(words:Union[str, list])->tuple:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
        # キーワード用の変数       
        word = words[0]
        word1 = words[1]
        keyword = ''
        # キーワードの数でＳＱＬを差し替える
        if len(words) == 2:
            # キーワード２つでタイトルとメモと著者から検索（word,word1）
            keyword = f"(book_table.title LIKE '%{word}%' OR book_table.memo LIKE '%{word}%' OR writer_table.writer LIKE '%{word}%') AND (book_table.title LIKE '%{word1}%' OR book_table.memo LIKE '%{word1}%'  OR writer_table.writer LIKE '%{word1}%')"
        else:
            # キーワード一つでタイトルとメモと著者から検索（words）
            keyword = f"book_table.title LIKE '%{words}%' OR book_table.memo LIKE '%{words}%' OR writer_table.writer LIKE '%{words}%'"
        # print(len(words))      
        # print(words)
        # print(word)
        # print(word1)
        # 著者名で検索（words）
        #keyword = f"writer_table.writer LIKE '%{words}%' "
        col_book = 'book_table.id, book_table.title, book_table.rubi, book_table.writer, book_table.publisher, book_table.memo, book_table.state'
        col_writer = 'writer_table.writer, writer_table.rubi'
        col_publisher = 'publisher_table.publisher'
        tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
        sql = f"SELECT {col_book},{col_writer},{col_publisher} FROM {tables} WHERE {keyword} limit 0,10"
        cur.execute(sql)
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
        print(data[1],data[7])
        count=i+1
    print(count,'件')
