# import MySQLdb
# import book_env
from dbc_abc import BookData
from typing import Union
from typing import Optional
from typing import Literal

class Book(BookData):
    '''書籍リスト
    引数は、並び替え、読書状態、表示件数（文字列、文字列、文字列）
    戻り値は、ＳＱＬの結果と総件数（タプル、タプル）
    '''        
    def list(self,sort:str,state:str) ->tuple[tuple,tuple[int]]:
        try:
            cur = self.conn.cursor()
            cur1 = self.conn.cursor()
            # テーブルのカラム
            col_book = 'book_table.id, book_table.title, book_table.rubi, book_table.writer, book_table.publisher, book_table.memo, book_table.state,book_table.disposal, book_table.create_time'
            col_writer = 'writer_table.writer, writer_table.rubi'
            col_publisher = 'publisher_table.publisher'
            # テーブル（外部結合）
            tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
            # WHERE句の条件分岐（全て/未読/読書中/既読）
            if state != '全て':
                read_state = f"book_table.state = '{state}'"
            else:
                read_state = "1=1" # 全件表示
            # ORDER BY（並び替え、デフォルトＩＤ降順）
            match sort:
                case 'タイトル昇順':
                    sorted = 'book_table.rubi ASC'
                case 'タイトル降順':
                    sorted = 'book_table.rubi DESC'
                case '著者昇順':
                    sorted = 'writer_table.rubi ASC'
                case '著者降順':
                    sorted = 'writer_table.rubi DESC'
                case 'ＩＤ昇順':
                    sorted = 'book_table.id ASC'
                case _:
                    sorted = 'book_table.id DESC'
            # SQL  limit 0,100  
            # sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book},{col_writer},{col_publisher} FROM {tables} WHERE {read_state} ORDER BY {sorted} LIMIT {limit}  "
            sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book},{col_writer},{col_publisher} FROM {tables} WHERE {read_state} ORDER BY {sorted}   "
            count = "SELECT FOUND_ROWS()"
            cur.execute(sql)
            cur1.execute(count)
            result = cur.fetchall()
            count_all = cur1.fetchone()
            return result,count_all

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            cur1.close()
            self.conn.close()

    '''書籍検索（スペース区切りで２つまで）
    引数は、検索ワード（文字列orリスト）と表示件数（文字列）
    戻り値は、ＳＱＬの結果と総件数（タプル、タプル）
    '''        
    def search(self,words:Union[str, list],sort:str)->tuple[tuple,tuple[int]]:
        try:
            cur = self.conn.cursor()
            cur1 = self.conn.cursor()
            # キーワード用の変数       
            keyword = ''
            # ORDER BY（並び替え、デフォルトＩＤ降順）
            match sort:
                case 'タイトル昇順':
                    sorted = 'book_table.rubi ASC'
                case 'タイトル降順':
                    sorted = 'book_table.rubi DESC'
                case '著者昇順':
                    sorted = 'writer_table.rubi ASC'
                case '著者降順':
                    sorted = 'writer_table.rubi DESC'
                case 'ＩＤ昇順':
                    sorted = 'book_table.id ASC'
                case _:
                    sorted = 'book_table.id DESC'
            # キーワードの数でＳＱＬを差し替える
            if len(words) == 2:
                word = words[0]
                word1 = words[1]
                # キーワード２つでタイトルとメモと著者から検索（word,word1）
                keyword = f"(book_table.title LIKE '%{word}%' OR book_table.memo LIKE '%{word}%' OR writer_table.writer LIKE '%{word}%') AND (book_table.title LIKE '%{word1}%' OR book_table.memo LIKE '%{word1}%'  OR writer_table.writer LIKE '%{word1}%')"
            else:
                word = words
                # キーワード一つでタイトルとメモと著者から検索（words）
                keyword = f"book_table.title LIKE '%{words}%' OR book_table.memo LIKE '%{words}%' OR writer_table.writer LIKE '%{words}%'"
            # 著者名で検索（words）
            #keyword = f"writer_table.writer LIKE '%{words}%' "
            col_book = 'book_table.id, book_table.title, book_table.rubi, book_table.writer, book_table.publisher, book_table.memo, book_table.state, book_table.disposal, book_table.create_time'
            col_writer = 'writer_table.writer, writer_table.rubi'
            col_publisher = 'publisher_table.publisher'
            tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
            # sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book},{col_writer},{col_publisher} FROM {tables} WHERE {keyword} LIMIT {limit} "
            sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book},{col_writer},{col_publisher} FROM {tables} WHERE {keyword} ORDER BY {sorted}  "
            count = "SELECT FOUND_ROWS()"
            cur.execute(sql)
            cur1.execute(count)
            result = cur.fetchall()
            count_all = cur1.fetchone()
            return result,count_all

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            cur1.close()
            self.conn.close()

    '''書籍データ（個別）
    引数は、ＩＤ（数値）
    戻り値は、ＳＱＬの結果（タプル）
    '''        
    def detail(self,id:int)->tuple:
        try:
            cur = self.conn.cursor()
            columns = 'book_table.id, book_table.title, book_table.rubi, book_table.writer,writer_table.writer, book_table.publisher, publisher_table.publisher,book_table.memo, book_table.state, book_table.create_time'
            tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id' 
            sql = f"SELECT {columns} FROM {tables} WHERE book_table.id = {id}"
            cur.execute(sql )
            result = cur.fetchall()
            return result

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''
    書籍データ追加し、生成されたＩＤを返す
    引数は、タイトル、フリガナ、著者ID、出版社ID、ＩＤ（テキスト、テキスト、数値、数値、数値）
    戻り値はタプル（自動生成されたＩＤ）
    '''        
    def insert(self,title:str,rubi:str,writer:int,publisher:int,memo:Optional[str],state:Literal['未読', '読書中', '既読'])->tuple:
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            #　書籍データ追加のinsert文
            sql = "INSERT INTO book_table(title,rubi,writer,publisher,memo,state) VALUES(%s, %s, %s, %s, %s, %s)"
            val = (title,rubi,writer,publisher,memo,state)
            # 自動生成されたＩＤを取得する
            sql_id ="SELECT LAST_INSERT_ID() FROM book_table"
            cur.execute(sql, val)
            cur.execute(sql_id )
            result = cur.fetchone()
        
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()
            return result    
        finally:
            cur.close()
            self.conn.close()

    '''書籍データ変更・更新
    引数は、タイトル、フリガナ、著者ID、出版社ID、状態、ＩＤ（テキスト、テキスト、数値、数値、テキスト、数値）
    戻り値はなし
    '''        
    def update(self,title:str,rubi:str,writer:int,publisher:int,memo:Optional[str],state:Literal['未読', '読書中', '既読'],id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            #sql = "INSERT INTO book_table(title,rubi,writer,publisher,memo) VALUES(title,rubi,writer,publisher,memo)"
            sql = "UPDATE book_table SET title=%s,rubi=%s,writer=%s,publisher=%s,memo=%s,state=%s WHERE id = %s "
            val = (title,rubi,writer,publisher,memo,state,id)
            cur.execute(sql, val)

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    '''書籍データ削除
    引数は、ＩＤ（数値）
    戻り値はなし
    '''        
    def delete(self,id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            sql = "DELETE FROM book_table WHERE id = %s "
            # データはタプルにする必要がある（ , を付けるとタプルに）
            cur.execute(sql, (id,))

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    # データ総数
    # def all_count(self) -> tuple:
    #     try:
    #         cur = self.conn.cursor()
    #         sql = "SELECT count(*) FROM book_table"
    #         cur.execute(sql )
    #         result = cur.fetchone()
    #         return result
    #     except Exception as e:
    #         print('データベースの接続に失敗しました。',e)
    #     finally:
    #         cur.close()
    #         self.conn.close()



