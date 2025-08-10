import MySQLdb
import book_env

# ブックテーブルのデータ全削除      
def book_clear() :
    conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
    try:
        cur = conn.cursor()
        sql = "truncate table book_table "
        cur.execute(sql)
    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

# ブックテーブルのデータ全削除      
def catalog_clear() :
    conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
    try:
        cur = conn.cursor()
        sql = "truncate table catalog_table "
        cur.execute(sql)
    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

# 削除書籍データ全削除
def del_book_clear() :
    conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
    try:
        cur = conn.cursor()
        sql = "truncate table disp_table "
        cur.execute(sql)
    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

# 出版社データ全削除
def publisher_clear() :
    conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
    try:
        cur = conn.cursor()
        sql = "truncate table publisher_table "
        cur.execute(sql)
    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()

# 著者データ全削除
def writer_clear() :
    conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)
    try:
        cur = conn.cursor()
        sql = "truncate table writer_table "
        cur.execute(sql)
    except Exception as e:
        print('データベースの接続に失敗しました。',e)
    finally:
        cur.close()
        conn.close()
