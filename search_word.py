import re
from typing import Union

# 検索フラグ（folder_searchが呼ばれているかの判定用）        
class SearchWord:
    def __init__(self):
        self.search_flag = False
    # getter
    @property
    def search_flag(self)-> bool :
        return self._search_flag
    # setter
    @search_flag.setter
    def search_flag(self,flg:bool):
        self._search_flag = flg
    ''' 
    検索ボタンクリック
    キーワードが１つか２つかの判定をする
    引数は文字列
    戻り値は、文字列orリスト
    '''
    def get_keyword(self,input_text:str)-> Union[str,list]:
        # 検索ワードを取得
        # 入力したキーワードに空白があるか判定
        if re.match(r'^.*\s.*$', input_text):
            # スペース区切りでリストにとる  
            words = words = input_text.split()
        else:
            # 単独キーワードの場合
            words = input_text
        return words 
