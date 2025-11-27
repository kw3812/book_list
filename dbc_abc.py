import MySQLdb
from book_env import USER, PASSWORD, HOST, DB, CHARSET
from abc import ABCMeta, abstractmethod
# import abc

class BookData(metaclass=ABCMeta):

    def __init__(self):
        self.conn = MySQLdb.connect(user=USER, passwd=PASSWORD, host=HOST, db=DB, charset=CHARSET)

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



