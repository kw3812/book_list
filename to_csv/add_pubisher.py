import sqlalchemy as sa
from sqlalchemy import create_engine
import pandas as pd
import jaconv 
import clear_dbc

df = pd.read_csv('D:\\xampp\\htdocs\\book_list\\doc\\publisher.csv')

# 必要な列を抽出して列名を変更
df = df[["出版社ID", "出版社名", "ﾙﾋﾞ", "備考"]]
df = df.set_axis(['id', 'publisher', 'rubi', 'memo'], axis=1)

# 半角カタカナを全角に
rubi = []
r = ''
for s in df['rubi']:
    #jaconv.h2z(str(s),kana=True, digit=False, ascii=False)
    r = jaconv.h2z(str(s))
    rubi.append(r)
df['rubi'] = rubi

# 現在のtableをクリア
clear_dbc.publisher_clear()

def add_publisher_list():
    try:
        url = 'mysql+pymysql://root:@localhost/book_list?charset=utf8'
        engine = sa.create_engine(url, echo=True)
        df.to_sql('publisher_table', engine, index=False,  if_exists='append')
    except Exception as e:
        print('データベースの接続に失敗しました。',e)

add_publisher_list()