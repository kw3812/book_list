import MySQLdb
from book_env import USER, PASSWORD, HOST, DB, CHARSET
from contextlib import contextmanager
from abc import ABCMeta, abstractmethod
from set_logger import get_logger2

class BookData(metaclass=ABCMeta):

    def __init__(self):
        self.conn = MySQLdb.connect(user=USER, passwd=PASSWORD, host=HOST, db=DB, charset=CHARSET)
        self.logger_name = get_logger2(__name__)
        
    @contextmanager
    def cursor(self):
        """
        カーソルのクローズを with で自動化する。
        失敗時はロールバック、成功時はコミット。
        """
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()

    @abstractmethod
    def list(self):
        pass
    @abstractmethod
    def detail(self):
        pass
    @abstractmethod
    def insert(self):
        pass
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def search(self):
        pass
    @abstractmethod
    def delete(self):
        pass



