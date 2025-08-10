from unittest import result
import MySQLdb
from typing import Optional
# import book_env
from dbc_abc import BookData
from dbc_apply import ApplyTo

class Writer(BookData,ApplyTo):
    # 一覧表示        
    def list(self,sort:str)->tuple:
        try:
            cur = self.conn.cursor()
            cols = 'id, writer, rubi, memo'
            match sort:
                case '著者昇順':
                    sort = 'rubi ASC'
                case '著者降順':
                    sort = 'rubi DESC'
                case 'ＩＤ昇順':
                    sort = 'id ASC'
                case _:
                    sort = 'id DESC'
            # sql = f"SELECT {cols} FROM writer_table ORDER BY {sort} LIMIT 0,30"
            sql = f"SELECT {cols} FROM writer_table ORDER BY {sort} "
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''個別表示
    引数はid（数値）
    戻り値はSQLの結果（タプル）
    '''
    def detail(self,id:int)->tuple:
        try:
            cur = self.conn.cursor()
            sql = f"SELECT * FROM writer_table WHERE id = {id}"
            cur.execute(sql )
            result = cur.fetchall()
            return result
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''特定の著者の書籍リスト
    引数はid（数値）
    戻り値はSQLの結果（タプル）
    '''        
    def book_list(self,id:int)->tuple:
        try:
            cur = self.conn.cursor()
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
            self.conn.close()

    '''著者検索
    引数は検索ワード（テキスト）
    戻り値はSQLの結果（タプル）
    '''        
    def search(self,word:str)->tuple:
        try:
            cur = self.conn.cursor()
                        # キーワード一つでタイトルとメモと著者から検索（words）
            keyword = f"writer LIKE '%{word}%'"
            sql = f"SELECT * FROM writer_table WHERE {keyword} "
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''著者データ追加
    引数は、著者、フリガナ、メモ（テキスト、テキスト、テキスト）
    戻り値は生成されたＩＤ（タプル）
    '''        
    def insert(self,writer:str,rubi:str,memo:str)->tuple:
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            sql = "INSERT INTO writer_table(writer,rubi,memo) VALUES(%s, %s, %s)"
            val = (writer,rubi,memo)
            sql_id ="SELECT LAST_INSERT_ID() FROM writer_table"
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

    '''著者データ変更・更新
    引数は、著者、フリガナ、メモ、ＩＤ（テキスト、テキスト、テキス、数値）
    戻り値はなし
    '''        
    def update(self,writer:str,rubi:str,memo:str,id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            sql = "UPDATE writer_table SET writer=%s,rubi=%s,memo=%s WHERE id = %s "
            val = (writer,rubi,memo,id)
            cur.execute(sql, val)

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    '''著者データ削除
    引数は、ＩＤ（数値）
    戻り値はなし
    '''        
    def delete(self,id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            sql = "DELETE FROM writer_table WHERE id = %s "
            # データはタプルにする必要がある（ , を付けるとタプルに）
            cur.execute(sql, (id,))
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    '''著者名からＩＤを求める
    引数は、検索ワード（著者名）（テキスト）
    戻り値は、ＩＤ（数値）or None
    '''        
    def search_id(self,word:str)->Optional[int]:
        try:
            cur = self.conn.cursor()
            sql = f"SELECT id, writer FROM writer_table WHERE writer = '{word}'"
            cur.execute(sql )
            result = cur.fetchall()
            return result[0][0]
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()


