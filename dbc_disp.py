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
        # mysqlに接続
        logger_name = get_logger2(__name__)
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            sql = "INSERT INTO disp_table(title,rubi,writer,publisher,memo,create_time) VALUES(%s, %s, %s, %s, %s, %s)"
            val = (title,rubi,writer,publisher,memo,create_time)
            cur.execute(sql, val)
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
            logger_name.error(f"Error: {e}", exc_info=True)
        else:
            logger_name.info(f"INSERT:廃棄テーブルに {title}を移動。 ")
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    '''書籍データ変更・更新
    引数は、タイトル、フリガナ、著者ID、出版社ID、ＩＤ（テキスト、テキスト、数値、数値、数値）
    戻り値はなし
    '''        
    def update(self,title:str,rubi:str,writer:int,publisher:int,memo:Optional[str],id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            #sql = "INSERT INTO book_table(title,rubi,writer,publisher,memo) VALUES(title,rubi,writer,publisher,memo)"
            sql = "UPDATE disp_table SET title=%s,rubi=%s,writer=%s,publisher=%s,memo=%s WHERE id = %s "
            val = (title,rubi,writer,publisher,memo,id)
            cur.execute(sql, val)

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    '''廃棄書籍データ（個別）
    引数は、ＩＤ（数値）
    戻り値は、ＳＱＬの結果（タプル）
    '''        
    def detail(self,id:int)->tuple:
        try:
            cur = self.conn.cursor()
            columns = 'disp_table.id, disp_table.title, disp_table.rubi, disp_table.writer,writer_table.writer, disp_table.publisher, publisher_table.publisher,disp_table.memo, disp_table.create_time'
            tables ='disp_table LEFT JOIN writer_table ON disp_table.writer = writer_table.id LEFT JOIN publisher_table ON disp_table.publisher = publisher_table.id' 
            sql = f"SELECT {columns} FROM {tables} WHERE disp_table.id = {id}"
            cur.execute(sql )
            result = cur.fetchall()
            return result

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''廃棄書籍データ削除
    引数は、ＩＤ（数値）
    戻り値はなし
    '''        
    def delete(self,id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            sql = "DELETE FROM disp_table WHERE id = %s "
            # データはタプルにする必要がある（ , を付けるとタプルに）
            cur.execute(sql, (id,))

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()
            
    def list(self):
        pass
    def search(self):
        pass
    # データ総数
    # def book_all(self) -> tuple:
    #     self.conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
    #     try:
    #         cur = self.conn.cursor()
    #         sql = "SELECT count(*) FROM disp_table"
    #         cur.execute(sql, )
    #         result = cur.fetchone()
    #         return result
    #     except Exception as e:
    #         print('データベースの接続に失敗しました。',e)
    #     finally:
    #         cur.close()
    #         self.conn.close()


