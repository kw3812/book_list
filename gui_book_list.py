import tkinter as tk
import tkinter.ttk as ttk
import re
from typing import Union
# リスト表示用ＳＱＬ
# キーワード検索用ＳＱＬ
from dbc_book import Book
# 書籍データ＋廃棄書籍のＳＱＬ
from dbc_union import UnionTable
# 個別（詳細）表示用ＳＱＬ
from gui_book_detail import Detail
# 詳細画面 
from gui_disp_detail import DispDetail
# 検索判定
from search_word import SearchWord

class BookList:
# ＳＱＬを受け取ってＧＵＩを表示する関数を呼ぶ
    def __init__(self):
        # 検索フラグのクラスを実装
        self.search_word = SearchWord()
        
        # 初期値の設定　--------------------------------------------------------------
        self.sorted = 'ID降順'
        self.state = '全て'
        # リスト表示用のＳＱＬを呼ぶ
        book = Book()
        self.result,self.count_all = book.list(self.sorted,self.state)

    def list_view(self):
        ''' --------------------------------------------------------------
        IDを元に詳細画面を開く
        disposalがTrueだったら廃棄書籍テーブル
        Falseだったら書籍テーブル    
        '''
        def _click_detail(event,id,disp):
            if disp == 1:
                disp = DispDetail(id)
                disp.detail_gui()
            else: 
                detai = Detail(id)       
                detai.gui_detail()

        # 検索処理---------------------------------------------------------
        def _click_search(event):
            # 検索フラグを立てる（ＳＱＬの判定用）
            self.search_word.search_flag = True
            _select_sql()

        # ソート用コンボボックス---------------------------------------------------
        def _sort_list(event):
            _select_sql()

        # 未読/読書中/既読の抽出--------------------------------------------------
        def _state_list(event):
            self.search_word. search_flag = False
            check_box.set(False)
            _select_sql()

        ''' --------------------------------------------------------------------
        checkboxの処理（廃棄を含める）
        get()メソッドは、tk.Checkbuttonではなく、tk.BooleanVar()にある
        '''        
        def _change_disp():
            seach_text.delete(0, tk.END) 
            self.search_word. search_flag = False
            _select_sql()

        # ボタンクリック時のＳＱＬ選択-------------------------------------------------
        def _select_sql():
            check_flg = check_box.get() 
            search_flag = self.search_word.search_flag
            input_text = seach_text.get().strip()
            if len(input_text) == 0 or len(input_text) == None:
                print('検索ワードが未入力です。')
            else:
                words = self.search_word.get_keyword(input_text)   
            state = combo_state.get()
            sort = combo_sort.get()
            # リスト表示用のＳＱＬを呼ぶ
            if  search_flag == True:
                if check_flg == True:
                    union = UnionTable(sort)
                    result,count_all = union.book_search(words)
                else:
                    book = Book()
                    result,count_all = book.search(words,sort)
            else:
                if check_flg == True:
                    union = UnionTable()
                    result,count_all = union.book_list(sort)
                else:
                    book = Book()
                    result,count_all = book.list(sort,state)
            # widgetの再作成とデータ件数表示
            count_i = gui_data(result,count_all) 

        '''     ------------------------------------------------------------
        解除ボタンクリック (初期値に戻す)
        検索テキストを削除
        コンボボックスを初期値に
        '''
        def _click_clear(event):
            check_box.set(False)
            self.search_word. search_flag = False
            seach_text.delete(0, tk.END) 
            combo_state.set('全て')
            combo_sort.set('ＩＤ降順')
            _select_sql()
            
    
        # ＧＵＩの作成  ----------------------------------------------
        root_li = tk.Toplevel()
        # root_li = tk.Tk()
        root_li.title('書籍データ')
        root_li.geometry('800x600+610+80')
        # 背景色
        back_color = '#FFCC66'
        # ボタンの色
        button_color = '#FF9933'
        # テキストボックスの色
        text_back_color = '#FFFFCC'
        root_li.configure(bg=back_color)

        '''
        コンボボックスとスクロールバーに適用するスタイルテーマ
        ここから背景色などを設定（どうも出来ないものもある）
        この方法しか色が変更できなかった
        '''
        style_li = ttk.Style()
        style_li.theme_use('default')

        # フレーム（検索テキスト・ボタン・コンボボックス・チェックボックス）
        frame_hed = tk.Frame(root_li, width=1300, height=40, pady=15, padx=0)
        frame_hed.configure(bg=back_color)
        # フレーム（ラベル）
        frame_lable = tk.Frame(root_li, width=1300, height=40, pady=5, padx=0)
        frame_lable.configure(bg=back_color)

        # scrollbar------------------
        #--------------

        # データのリスト表示部分
        frame_hed.grid(row=0, column=0, sticky=tk.W)

        # 件数表示用
        id_int = tk.IntVar()
        count_id = tk.Entry(frame_hed, width=10, bg=text_back_color, textvariable=id_int, justify="center")
        count_id.grid(row=0, column=0, padx=5, sticky=tk.W)
        # 検索用テキスト
        seach_text = tk.Entry(frame_hed, width=30, bg=text_back_color)
        seach_text.grid(row=0, column=1, padx=2, sticky=tk.E)
        # 検索ボタン
        button_search = tk.Button(frame_hed, width=5, bg=button_color, text='検索')
        #<ButtonPress> 左クリックイベント
        # リストをクリアする関数と、検索関数（ＳＱＬ）を呼ぶ
        button_search.bind('<ButtonPress>',_click_search)
        button_search.grid(row=0, column=2, padx=0, sticky=tk.W)
        # 解除（初期化）ボタン
        button_clear = tk.Button(frame_hed, width=5, padx=2, bg=button_color, text='解除')
        #<ButtonPress> 左クリックイベント
        button_clear.bind('<ButtonPress>',_click_clear)
        # button_clear.bind("<ButtonPress>", click_clear, "+")
        button_clear.grid(row=0, column=3, padx=2, sticky=tk.W)

        # state Combobox(styleを先に設定)
        style_li.configure('default.TCombobox',fieldbackground=text_back_color)
        state_value = ('全て','未読', '読書中', '既読')
        combo_state = ttk.Combobox(frame_hed,width=10, values= state_value, style='default.TCombobox')
        #combo_state.insert(0,'全て')
        combo_state.set('全て')
        # 複数の関数を指定する 
        combo_state.bind('<<ComboboxSelected>>',_state_list)
        # combo_state.bind('<<ComboboxSelected>>',sort_list, "+")
        combo_state.grid(row=0, column=4, padx=20 )

        # sort Combobox
        sort_value = ('タイトル昇順', 'タイトル降順','著者昇順','著者降順','ＩＤ降順','ＩＤ昇順')
        combo_sort = ttk.Combobox(frame_hed,width=10, values= sort_value , style='default.TCombobox' )
        #combo_sort.insert(0,'ＩＤ降順')
        combo_sort.set('ＩＤ降順')
        combo_sort.bind('<<ComboboxSelected>>',_sort_list)
        #combo_sort.bind('<<ComboboxSelected>>',  sort_list, "+")
        combo_sort.grid(row=0, column=5)
        #　checkbox
        check_box = tk.BooleanVar(value =False)
        check_disp = tk.Checkbutton(frame_hed, text = '廃棄を含める', variable = check_box ,background=back_color, command=_change_disp)
        check_disp.grid(row=0, column=6, padx=20)


        # Treeviewの作成
        columns = ("ID", "タイトル", "著者", "出版社", "状態")
        tree = ttk.Treeview(root_li, columns=columns, show='headings', height=25 )
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#FF6633", font=("",12))
        style.configure("Treeview", background="#FFFFCC", font=("",12))

        # 各カラムのヘッダーテキストと幅を設定
        tree.heading("ID", text="ID")
        tree.column("ID", width=60, anchor=tk.CENTER)

        tree.heading("タイトル", text="タイトル")
        tree.column("タイトル", width=300)

        tree.heading("著者", text="著者")
        tree.column("著者", width=150)

        tree.heading("出版社", text="出版社")
        tree.column("出版社", width=150)

        tree.heading("状態", text="状態")
        tree.column("状態", width=100, anchor=tk.CENTER)

        tree.grid(row=1, column=0, sticky='nsew', padx=10)

        # スクロールバーの設定
        scrollbar = ttk.Scrollbar(root_li, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

        # Treeviewにデータを挿入
        def gui_data(result, count_all):
            all_count = count_all[0]
            id_int.set(f'{all_count}件')              
            # Treeviewの既存データをクリア
            tree.delete(*tree.get_children())
            for data in result:
                # 項目ごとにリストにとる
                ids = data[0]
                titles = data[1] 
                states = data[6]
                # 廃棄書籍テーブルにはstateがないための処理
                if check_box.get():
                    writers = data[8] 
                    publishers = data[10] 
                    disposals = data[6] 
                    states = disposals
                else:
                    writers = data[9] 
                    publishers = data[11] 
                    states = data[6] 
                    disposals = data[7] 
                if states == 0:
                    states = '存'
                elif states == 1  :  
                    states = '廃'
                tree.insert('', tk.END, values=[ids, titles, writers, publishers, states])

            # Treeviewの行がクリックされたときのイベントバインド
            def _on_item_click(event):
                item = tree.selection()[0]
                list_id = tree.item(item, 'values')[0]
                _click_detail(event, list_id,disposals)

            tree.bind('<ButtonRelease-1>', _on_item_click)

        gui_data(self.result, self.count_all)
        
        root_li.mainloop() 

if __name__ == '__main__':
    list = BookList()
    list.list_view()
