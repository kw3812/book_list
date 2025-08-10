import sqlalchemy as sa
from sqlalchemy import create_engine
import pandas as pd
import jaconv 
import clear_dbc

#ＣＳＶ読み込み
df = pd.read_csv('D:\\xampp\\htdocs\\book_list\\doc\\catalog.csv')
# 必要な列を抽出して列名を変更
# df = df[["タイトル", "ソート用", "著者ID", "出版社ID", "内容", "読／未"]]
df = df.set_axis(['title', 'event', 'publisher', 'store', 'category', 'etc', 'year'], axis=1)


# 現在のbook_tableをクリア
clear_dbc.catalog_clear()

# データフレームをＭＹＳＱＬのテーブルに書き込む
def add_catalog_list():
    try:
        url = 'mysql+pymysql://root:@localhost/book_list?charset=utf8'
        engine = sa.create_engine(url, echo=True)
        df.to_sql('catalog_table', engine, index=False,  if_exists='append')
    except Exception as e:
        print('データベースの接続に失敗しました。',e)

add_catalog_list()