from typing import Optional
from dbc_abc import BookData
from datetime import datetime
from set_logger import get_logger2

class Disp(BookData):

    '''
    書籍テーブルから廃棄書籍に移動（インサート部分）
    引数にタイトル・フリガナ・著者ID・出版社ID・メモをとる。
    戻り値なし
    '''
    def insert(self,title:str,rubi:str,writer:int,publisher:int,memo:Optional[str],create_time:datetime):
        sql = "INSERT INTO disp_table(title,rubi,writer,publisher,memo,create_time) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (title,rubi,writer,publisher,memo,create_time)
        try:
            with self.cursor() as cur:
                cur.execute(sql, val)
                self.logger_name.info(f"INSERT:廃棄テーブルに {title}を移動。 ")
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
            self.logger_name.error(f"{title}の廃棄テーブル移動に失敗  {e}", exc_info=True)

    '''書籍データ変更・更新
    引数は、タイトル、フリガナ、著者ID、出版社ID、ＩＤ（テキスト、テキスト、数値、数値、数値）
    戻り値はなし
    '''        
    def update(self,title:str,rubi:str,writer:int,publisher:int,memo:Optional[str],id:int):
        #sql = "INSERT INTO book_table(title,rubi,writer,publisher,memo) VALUES(title,rubi,writer,publisher,memo)"
        sql = "UPDATE disp_table SET title=%s,rubi=%s,writer=%s,publisher=%s,memo=%s WHERE id = %s "
        val = (title,rubi,writer,publisher,memo,id)
        try:
            with self.cursor() as cur:
                cur.execute(sql, val)

        except Exception as e:
            print('データベースの接続に失敗しました。',e)

    '''廃棄書籍データ（個別）
    引数は、ＩＤ（数値）
    戻り値は、ＳＱＬの結果（タプル）
    '''        
    def detail(self,id:int)->tuple:
        columns = 'disp_table.id, disp_table.title, disp_table.rubi, disp_table.writer,writer_table.writer, disp_table.publisher, publisher_table.publisher,disp_table.memo, disp_table.create_time'
        tables ='disp_table LEFT JOIN writer_table ON disp_table.writer = writer_table.id LEFT JOIN publisher_table ON disp_table.publisher = publisher_table.id' 
        sql = f"SELECT {columns} FROM {tables} WHERE disp_table.id = {id}"
        try:
            with self.cursor() as cur:
                cur.execute(sql )
                result = cur.fetchall()
                return result

        except Exception as e:
            print('データベースの接続に失敗しました。',e)

    '''廃棄書籍データ削除
    引数は、ＩＤ（数値）
    戻り値はなし
    '''        
    def delete(self,id:int):
        sql = "DELETE FROM disp_table WHERE id = %s "
        try:
            with self.cursor() as cur:
                # データはタプルにする必要がある（ , を付けるとタプルに）
                cur.execute(sql, (id,))

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
            
    def list(self):
        pass
    def search(self):
        pass

