import MySQLdb
import book_env
from abc import ABCMeta, abstractmethod
# import abc

class BookData(metaclass=ABCMeta):

    def __init__(self):
        self.conn = MySQLdb.connect(user=book_env.user, passwd=book_env.passwd, host=book_env.host, db=book_env.db, charset=book_env.charset)

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



