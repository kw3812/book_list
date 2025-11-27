from dbc_book import Book
# 書籍データ＋廃棄書籍のＳＱＬ
from dbc_union import UnionTable
# 個別（詳細）表示用ＳＱＬ
from gui_book_detail import Detail
# 詳細画面 
from gui_disp_detail import DispDetail

class BookListEvent:
    def __init__(self):
        pass
    ''' --------------------------------------------------------------
    IDを元に詳細画面を開く
    disposalがTrueだったら廃棄書籍テーブル
    Falseだったら書籍テーブル    
    '''
    def click_detail(self,id,disp):
        if disp == 1:
            disp = DispDetail(id)
            disp.detail_gui()
        else: 
            detai = Detail(id)       
            detai.gui_detail()

    # ボタンクリック時のＳＱＬ選択-------------------------------------------------
    def select_sql(self,check_flg, search_flag, state, sort, words):
        # リスト表示用のＳＱＬを呼ぶ
        if  search_flag == True:
            if check_flg == True:
                union = UnionTable()
                result,count_all = union.search(words)
            else:
                book = Book()
                result,count_all = book.search(words,sort)
        else:
            if check_flg == True:
                union = UnionTable()
                result,count_all = union.list(sort)
            else:
                book = Book()
                result,count_all = book.list(sort,state)
                
        return result,count_all         
