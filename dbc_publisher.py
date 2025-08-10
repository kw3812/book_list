# import book_env
# import re
# import MySQLdb
from typing import Optional
from dbc_abc import BookData
from dbc_apply import ApplyTo

#   基底クラス BookDataとApplyToを継承
class Publisher(BookData, ApplyTo):
    '''
    出版社リスト（オーバーライド）
    param sort(並び順)
    return result（データリスト）
    '''
    def list(self,sort:str)->tuple:
        try:
            cur = self.conn.cursor()
            cols = 'id, publisher, rubi, memo'
            match sort:
                case '出版社昇順':
                    sort = 'rubi ASC'
                case '出版社降順':
                    sort = 'rubi DESC'
                case 'ＩＤ昇順':
                    sort = 'id ASC'
                case _:
                    sort = 'id DESC'
            # sql = f"SELECT {cols} FROM publisher_table ORDER BY {sort} LIMIT 0,30"
            sql = f"SELECT {cols} FROM publisher_table ORDER BY {sort} "

            cur.execute(sql)
            result = cur.fetchall()
            return result
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''
    出版社データ（個別）
    param ID
    return result（該当データ）
    '''        
    def detail(self,id:int)->tuple:
        try:
            cur = self.conn.cursor()
            sql = f"SELECT * FROM publisher_table WHERE id = {id}"
            cur.execute(sql )
            result = cur.fetchall()
            return result
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''
    出版社検索
    param word(検索ワード)
    return result（データリスト）
    '''        
    def search(self,word:str)->tuple:
        try:
            cur = self.conn.cursor()
                        # キーワード一つでタイトルとメモと著者から検索（words）
            keyword = f"publisher LIKE '%{word}%' OR memo LIKE '%{word}%'"
            sql = f"SELECT * FROM publisher_table WHERE {keyword} "
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''
    出版社データ追加
    param publiser(社名), rubi（カナ）, memo（メモ）
    return --
    '''        
    def insert(self,publisher:str,rubi:str,memo:str):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            sql = "INSERT INTO publisher_table(publisher,rubi,memo) VALUES(%s, %s, %s)"
            val = (publisher,rubi,memo)
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

    '''
    出版社データ変更・更新
    param publiser(社名), rubi（カナ）, memo（メモ）, ID
    return --
    '''        
    def update(self,publisher:str,rubi:str,memo:str,id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            sql = "UPDATE publisher_table SET publisher=%s,rubi=%s,memo=%s WHERE id = %s "
            val = (publisher,rubi,memo,id)
            cur.execute(sql, val)

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    '''
    出版社データ削除
    param ID
    return --
    '''        
    def delete(self,id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            sql = "DELETE FROM publisher_table WHERE id = %s "
            # データはタプルにする必要がある（ , を付けるとタプルに）
            cur.execute(sql, (id,))

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    '''
    出版社名からＩＤを求める
    param word(社名)
    return result（ID or None）
    '''        
    def search_id(self,word:str)->Optional[int]:
        try:
            cur = self.conn.cursor()
            sql = f"SELECT id, publisher FROM publisher_table WHERE publisher = '{word}'"
            cur.execute(sql )
            result = cur.fetchall()
            return result[0][0]
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''
    特定の出版社の書籍リスト
    param ID
    return result（該当書籍リスト）
    '''        
    def book_list(self,id:int)->tuple:
        try:
            cur = self.conn.cursor()
            col_book = 'book_table.id, book_table.title, book_table.writer, book_table.publisher'
            col_writer = 'writer_table.id, writer_table.writer '
            col_publisher = 'publisher_table.id, publisher_table.publisher'
            # テーブル（外部結合）
            tables ='book_table LEFT JOIN writer_table ON book_table.writer = writer_table.id LEFT JOIN publisher_table ON book_table.publisher = publisher_table.id'
            sql = f"SELECT {col_book},{col_writer},{col_publisher} FROM {tables} WHERE book_table.publisher = {id}"
            cur.execute(sql )
            result = cur.fetchall()
            return result

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()




