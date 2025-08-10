import sqlalchemy as sa
from sqlalchemy import create_engine
import pandas as pd
import jaconv 
import clear_dbc


df = pd.read_csv('D:\\xampp\\htdocs\\book_list\\doc\\del_book.csv')

# 必要な列を抽出して列名を変更
df = df[["タイトル", "ソート用", "著者ID", "出版社ID", "内容"]]
df = df.set_axis(['title', 'rubi', 'writer', 'publisher', 'memo'], axis=1)

# 半角カタカナを全角に
rubi = []
r = ''
for s in df['rubi']:
    #jaconv.h2z(str(s),kana=True, digit=False, ascii=False)
    r = jaconv.h2z(str(s))
    rubi.append(r)
df['rubi'] = rubi

# 現在のtableをクリア
clear_dbc.del_book_clear()

# データフレームをＭＹＳＱＬのテーブルに書き込む
def add_book_list():
    try:
        url = 'mysql+pymysql://root:@localhost/book_list?charset=utf8'
        engine = sa.create_engine(url, echo=True)
        df.to_sql('disp_table', engine, index=False,  if_exists='append')
    except Exception as e:
        print('データベースの接続に失敗しました。',e)

add_book_list()