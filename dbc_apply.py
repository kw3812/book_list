from abc import ABCMeta, abstractmethod

class ApplyTo(metaclass=ABCMeta):

    @abstractmethod
    def search_id(self):
        pass
    @abstractmethod
    def book_list(self):
        pass

