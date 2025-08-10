import sqlalchemy as sa
import pandas as pd
from sql import book_json as bj

# 該当テーブルのデータからデータフレームを作成
def convert_json(table_name:str) -> pd.DataFrame:
    rows = bj.book_list(table_name)
    id = []
    title= []
    writer = []
    writer_rubi = []
    publisher = []
    memo = []
    create_time = []
    disposal = []
    for row in rows:
        id.append(row[0])
        title.append(row[1])
        memo.append(row[4])   
        create_time.append(row[5])
        writer.append(row[6])
        writer_rubi.append(row[7])
        publisher.append(row[8])
        if table_name == 'book_table':
            disposal.append('◯')
        else :
            disposal.append('☓')
    # pandasでデータ処理
    columns =["id", "title", "writer",  "rubi", "publisher","disposal","create_time"]
    df = pd.DataFrame(columns=columns)
    df['id'] = id
    df['title'] = title
    df['writer'] = writer
    df['rubi'] = writer_rubi
    df['publisher'] = publisher
    df['memo'] = memo
    df['create_time'] = create_time
    df['disposal'] = disposal
    # df = df.sort_values('id',ascending=False)

    return df

# データフレームを結合してＪＳＯＮに変換する
def json_write(df_disp:pd.DataFrame, df_book:pd.DataFrame):
    df_table = pd.concat([df_disp, df_book], axis=0, ignore_index=True)
    # print(df_table)
   # 降順で並び替え
    # df_table = df_table.sort_values('disposal',ascending=True)
    # df_table.sort_values(by=["disposal","id"], ascending=[True, False]) 
    path = 'D:\\xampp/htdocs/book_list/book.json'
    # jsonに変換（force_ascii日本語対応   orient='values'データのみ出力 ）
    json = df_table.to_json(path,orient='values',force_ascii=False)
    # print(json)

df_disp = convert_json('disp_table')
df_book = convert_json('book_table')
# print(df_book)
json_write(df_disp, df_book)

# if __name__ == '__main__':      
#     result = convert_json('book_table')
