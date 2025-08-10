import MySQLdb
import book_env

def seach_writer(word:str)->tuple:
    try:
        conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
        cur = conn.cursor()
                    # キーワード一つでタイトルとメモと著者から検索（words）
        keyword = f"writer LIKE '%{word}%'"
        sql = f"SELECT * FROM writer_table WHERE {keyword} "
        cur.execute(sql)
        result = cur.fetchall()
        return result

    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    word = "鈴木"
    result = seach_writer(word)
    for data in result:
        print(data[1])
