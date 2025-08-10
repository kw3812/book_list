from dbc_abc import BookData
from typing import Union
from typing import Optional
from typing import Literal

class Catalog(BookData):
    '''図録・イベント冊子などリスト
    pram sort（並び順）
    retur result, count_all（リストデータ、件数）
    '''        
    def list(self,sort:str) ->tuple[tuple,tuple[int]]:
        try:
            cur = self.conn.cursor()
            cur1 = self.conn.cursor()
            # テーブルのカラム
            col_book = 'id, title, event, publisher, store, category, year'
            sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book} FROM catalog_table ORDER BY year {sort} "
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


    ''' 個別データ
    pram id
    return result(個別データ)
    '''        
    def detail(self,id:int)->tuple:
        try:
            cur = self.conn.cursor()
            sql = f"SELECT * FROM catalog_table WHERE id = {id}"
            cur.execute(sql )
            result = cur.fetchall()
            return result

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        finally:
            cur.close()
            self.conn.close()

    '''
    データ追加し、生成されたＩＤを返す
    param title, rubi, event, publisher, store, etc
    retur result (last_inert_id)
    '''        
    def insert(self, title:str, event:str, publisher:str, store:str, category:str, etc:Optional[str], year:str)->tuple:
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            #　書籍データ追加のinsert文
            sql = "INSERT INTO catalog_table(title, event, publisher, store, category, etc, year) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            val = (title, event, publisher, store, category, etc, year)
            # 自動生成されたＩＤを取得する
            sql_id ="SELECT LAST_INSERT_ID() FROM catalog_table"
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

    ''' データ変更・更新
    param title, rubi, event, publisher, store, etc ,id
    return void
    '''        
    def update(self,title:str,event:str, publisher:str, store:str, category:str, etc:str, year:str, id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            sql = "UPDATE catalog_table SET title=%s,event=%s,publisher=%s,store=%s,category=%s,etc=%s,year=%s WHERE id = %s "
            val = (title, event, publisher, store, category, etc, year ,id)
            cur.execute(sql, val)

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    ''' データ削除
    pram id
    return void
    '''        
    def delete(self,id:int):
        # mysqlに接続
        try:
            cur = self.conn.cursor()
            # ＳＱＬ　
            sql = "DELETE FROM catalog_table WHERE id = %s "
            # データはタプルにする必要がある（ , を付けるとタプルに）
            cur.execute(sql, (id,))

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
        else:
            self.conn.commit()    
        finally:
            cur.close()
            self.conn.close()

    ''' 検索
    parm word, column(検索文字列, 検索カラム)
    return result,count_all(リストデータ, 件数)
    '''        
    def search(self,words:str, column:str)->tuple[tuple,tuple[int]]:
        try:
            cur = self.conn.cursor()
            cur1 = self.conn.cursor()
            # キーワード一つでタイトルとメモと著者から検索（words）
            # if column == 'title':
            #     keyword = f"title LIKE '%{words}%'"
            # elif column == 'store':    
            #     keyword = f"store LIKE '%{words}%'"
            col_book = 'id, title, event, publisher, store, category, year'
            sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book} FROM catalog_table WHERE {column} LIKE '%{words}%' ORDER BY year DESC "
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


if __name__ == '__main__':
    catalog = Catalog()
    sort = 'DESC'
    id = '10'
    
    result = catalog.list(sort)
    # result = catalog.detail(id)

    # print(result)
