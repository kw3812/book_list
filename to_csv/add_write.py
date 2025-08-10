import sqlalchemy as sa
from sqlalchemy import create_engine
import pandas as pd
import jaconv 
import clear_dbc

df = pd.read_csv('D:\\xampp\\htdocs\\book_list\\doc\\writer.csv')

# 必要な列を抽出して列名を変更
df = df[["著者ＩＤ", "著者名", "ﾌﾘｶﾞﾅ", "メモ"]]
df = df.set_axis(['id', 'writer', 'rubi', 'memo'], axis=1)

# 半角カタカナを全角に
rubi = []
r = ''
for s in df['rubi']:
    #jaconv.h2z(str(s),kana=True, digit=False, ascii=False)
    r = jaconv.h2z(str(s))
    rubi.append(r)
df['rubi'] = rubi

# 現在のtableをクリア
clear_dbc.writer_clear()

def add_writer_list():
    try:
        url = 'mysql+pymysql://root:@localhost/book_list?charset=utf8'
        engine = sa.create_engine(url, echo=True)
        df.to_sql('writer_table', engine, index=False,  if_exists='append')
    except Exception as e:
        print('データベースの接続に失敗しました。',e)

add_writer_list()