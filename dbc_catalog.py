from dbc_abc import BookData
from typing import Optional

class Catalog(BookData):
    '''図録・イベント冊子などリスト
    pram sort（並び順）
    retur result, count_all（リストデータ、件数）
    '''        
    def list(self,sort:str) ->tuple[tuple,tuple[int]]:
        # テーブルのカラム
        col_book = 'id, title, event, publisher, store, category, year'
        sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book} FROM catalog_table ORDER BY year {sort} "
        count = "SELECT FOUND_ROWS()"
        try:
            with self.cursor() as cur: 
                cur.execute(sql)
                result = cur.fetchall()
                cur.execute(count)
                count_all = cur.fetchone()
                return result,count_all

        except Exception as e:
            print('データベースの接続に失敗しました。',e)

    ''' 個別データ
    pram id
    return result(個別データ)
    '''        
    def detail(self,id:int)->tuple:
        sql = "SELECT * FROM catalog_table WHERE id = %s"
        try:
            with self.cursor() as cur:
                cur.execute(sql, (id,) )
                result = cur.fetchall()
                return result

        except Exception as e:
            print('データベースの接続に失敗しました。',e)

    '''
    データ追加し、生成されたＩＤを返す
    param title, rubi, event, publisher, store, etc
    retur result (last_inert_id)
    '''        
    def insert(self, title:str, event:str, publisher:str, store:str, category:str, etc:Optional[str], year:str)->tuple:
        #　書籍データ追加のinsert文
        sql = "INSERT INTO catalog_table(title, event, publisher, store, category, etc, year) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        val = (title, event, publisher, store, category, etc, year)
        # 自動生成されたＩＤを取得する
        sql_id ="SELECT LAST_INSERT_ID() FROM catalog_table"
        try:
            with self.cursor() as cur:
                cur.execute(sql, val)
                cur.execute(sql_id )
                result = cur.fetchone()
                self.logger_name.info(f"{title}を追加しました。 ")
                return result    
        
        except Exception as e:
            print('データベースの接続に失敗しました。',e)
            self.logger_name.error(f"{title}を追加に失敗しました。 ")

    ''' データ変更・更新
    param title, rubi, event, publisher, store, etc ,id
    return void
    '''        
    def update(self,title:str,event:str, publisher:str, store:str, category:str, etc:str, year:str, id:int):
        sql = "UPDATE catalog_table SET title=%s,event=%s,publisher=%s,store=%s,category=%s,etc=%s,year=%s WHERE id = %s "
        val = (title, event, publisher, store, category, etc, year ,id)
        try:
            with self.cursor() as cur:
                cur.execute(sql, val)

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
            self.logger_name.error(f"{title}を更新に失敗しました。 ")

    ''' データ削除
    pram id
    return void
    '''        
    def delete(self,id:int):
        sql = "DELETE FROM catalog_table WHERE id = %s "
        try:
            with self.cursor() as cur:
                # データはタプルにする必要がある（ , を付けるとタプルに）
                cur.execute(sql, (id,))

        except Exception as e:
            print('データベースの接続に失敗しました。',e)
            self.logger_name.error(f"{id}データの削除に失敗しました。 ")

    ''' 検索
    parm word, column(検索文字列, 検索カラム)
    return result,count_all(リストデータ, 件数)
    '''        
    def search(self,words:str, column:str)->tuple[tuple,tuple[int]]:
        # キーワード一つでタイトルとメモと著者から検索（words）
        # if column == 'title':
        #     keyword = f"title LIKE '%{words}%'"
        # elif column == 'store':    
        #     keyword = f"store LIKE '%{words}%'"
        col_book = 'id, title, event, publisher, store, category, year'
        sql = f"SELECT SQL_CALC_FOUND_ROWS {col_book} FROM catalog_table WHERE {column} LIKE '%{words}%' ORDER BY year DESC "
        count = "SELECT FOUND_ROWS()"
        try:
            with self.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()
                cur.execute(count)
                count_all = cur.fetchone()
                return result,count_all

        except Exception as e:
            print('データベースの接続に失敗しました。',e)

if __name__ == '__main__':
    catalog = Catalog()
    sort = 'DESC'
    id = '10'
    
    result = catalog.list(sort)
    # result = catalog.detail(id)

    # print(result)
