# NEXT・BACK　ボタン関連クラス
class PageChange:
    def __init__(self):
        self._start_count = 0
        self._add_count = 50
    # getter
    @property
    def start_count(self)-> int :
        return self._start_count
    # setter
    @start_count.setter
    def start_count(self, s_count:int):
        self._start_count = s_count
    # getter
    @property
    def add_count(self)-> int :
        return self._add_count
    # setter
    @add_count.setter
    def add_count(self, add:int):
        self._add_count = add

    # NEXTボタンの処理（click_next関数に呼ばれる）
    def count_next(self,count:int) -> str:
        start_count = self._start_count
        add_count = self._add_count
        if count < add_count:
            start_count = 0
        elif start_count + add_count*2 < count :
            start_count = start_count + add_count
        else:
            start_count = count - add_count
            print('最終データ')
        self._start_count= start_count
        limit = f'{start_count},{add_count}'
        print(limit,count)
        return  limit
    # BACKボタンの処理 （click_back関数に呼ばれる）        
    def count_back(self) -> str:
        start_count = self._start_count
        add_count = self._add_count
        if start_count > 0:
            if start_count < add_count:
                start_count = 0
            else:    
                start_count = start_count - add_count
        else:
            start_count = 0
            print('最初のデータ')   
        self._start_count= start_count
        limit = f'{start_count},{add_count}'
        return  limit
