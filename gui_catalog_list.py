import tkinter as tk
import tkinter.ttk as ttk
import re
from typing import Union
# リスト表示用ＳＱＬ
# キーワード検索用ＳＱＬ
from dbc_catalog import Catalog
# 個別（詳細）表示用ＳＱＬ
from gui_catalog_detail import Detail
# 検索判定
from search_word import SearchWord

class CatalogList:
# ＳＱＬを受け取ってＧＵＩを表示する関数を呼ぶ
    def __init__(self):
        # 検索フラグのクラスを実装
        self.search_word = SearchWord()
        
        # 初期値の設定　--------------------------------------------------------------
        self.sorted = 'DESC'
        # リスト表示用のＳＱＬを呼ぶ
        catalog = Catalog()
        self.result,self.count_all = catalog.list(self.sorted)

    def list_view(self):
        ''' --------------------------------------------------------------
        IDを元に詳細画面を開く
        '''
        def _click_detail(event,id):
            detai = Detail(id)       
            detai.gui_detail()

        # 検索処理---------------------------------------------------------
        def _click_search(event):
            # 検索フラグを立てる（ＳＱＬの判定用）
            self.search_word.search_flag = True
            _select_sql()

        # ソート用コンボボックス---------------------------------------------------
        def _sort_list(event):
            self.sorted = 'DESC'
            _select_sql()


        # ボタンクリック時のＳＱＬ選択-------------------------------------------------
        def _select_sql():
            # 検索フラグ
            search_flag = self.search_word.search_flag
            # ソート    
            sort = combo_sort.get()
            # リスト表示用のＳＱＬを呼ぶ
            if  search_flag == True:
                input_text = seach_text.get().strip()
                if len(input_text) == 0 or len(input_text) == None:
                    print('検索ワードが未入力です。')
                colmun = combo_col.get()
                catalog = Catalog()
                result,count_all = catalog.search(input_text, colmun)
            else:
                catalog = Catalog()
                result,count_all = catalog.list(sort)
            # widgetの再作成とデータ件数表示
            count_i = gui_data(result,count_all) 

        '''     ------------------------------------------------------------
        解除ボタンクリック (初期値に戻す)
        検索テキストを削除
        コンボボックスを初期値に
        '''
        def _click_clear(event):
            self.search_word. search_flag = False
            seach_text.delete(0, tk.END) 
            combo_sort.set('DESC')
            _select_sql()
            
    
        # ＧＵＩの作成  ----------------------------------------------
        root_li = tk.Toplevel()
        # root_li = tk.Tk()
        root_li.title('その他書籍データ')
        root_li.geometry('960x600+610+80')
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
        frame_hed = tk.Frame(root_li, width=960, height=40, pady=15, padx=0)
        frame_hed.configure(bg=back_color)
        # フレーム（ラベル）
        frame_lable = tk.Frame(root_li, width=960, height=40, pady=5, padx=0)
        frame_lable.configure(bg=back_color)

        # scrollbar------------------
        #--------------

        # データのリスト表示部分
        frame_hed.grid(row=0, column=0, sticky=tk.W)

        # 件数表示用    ---------------------------------------------------------------------
        id_int = tk.IntVar()
        count_id = tk.Entry(frame_hed, width=10, bg=text_back_color, textvariable=id_int, justify="center")
        count_id.grid(row=0, column=0, padx=5, sticky=tk.W)
        # 検索用テキスト
        seach_text = tk.Entry(frame_hed, width=30, bg=text_back_color)
        seach_text.grid(row=0, column=1, padx=2, sticky=tk.E)

        # column select Combobox
        col_value = ('title', 'event', 'store', 'category', 'year')
        combo_col = ttk.Combobox(frame_hed,width=10, values= col_value , style='default.TCombobox' )
        #combo_col.insert(0,'ＩＤ降順')
        combo_col.set('title')
        # combo_col.bind('<<ComboboxSelected>>',_sort_list)
        #combo_col.bind('<<ComboboxSelected>>',  col_list, "+")
        combo_col.grid(row=0, column=2, padx=5)
        # 検索ボタン
        button_search = tk.Button(frame_hed, width=5, bg=button_color, text='検索')
        #<ButtonPress> 左クリックイベント
        # リストをクリアする関数と、検索関数（ＳＱＬ）を呼ぶ
        button_search.bind('<ButtonPress>',_click_search)
        button_search.grid(row=0, column=3, padx=5, sticky=tk.W)

        # sort Combobox ---------------------------------------------------------------------
        sort_value = ('ASC', 'DESC')
        combo_sort = ttk.Combobox(frame_hed,width=10, values= sort_value , style='default.TCombobox' )
        #combo_sort.insert(0,'ＩＤ降順')
        combo_sort.set('DESC')
        combo_sort.bind('<<ComboboxSelected>>',_sort_list)
        # combo_sort.bind('<<ComboboxSelected>>',  sort_list, "+")
        combo_sort.grid(row=0, column=5, padx=5)

        # 解除（初期化）ボタン  -----------------------------------------------------------------
        button_clear = tk.Button(frame_hed, width=5, padx=2, bg=button_color, text='解除')
        #<ButtonPress> 左クリックイベント
        button_clear.bind('<ButtonPress>',_click_clear)
        # button_clear.bind("<ButtonPress>", click_clear, "+")
        button_clear.grid(row=0, column=4, padx=5, sticky=tk.W)

        # Treeviewの作成
        columns = ("ID", "Title", "Store", "Category", "year")
        tree = ttk.Treeview(root_li, columns=columns, show='headings', height=25 )
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#FF6633", font=("",12))
        style.configure("Treeview", background="#FFFFCC", font=("",12))

        # 各カラムのヘッダーテキストと幅を設定
        tree.heading("ID", text="ID")
        tree.column("ID", width=60, anchor=tk.CENTER)

        tree.heading("Title", text="タイトル")
        tree.column("Title", width=460)

        tree.heading("Store", text="入手先")
        tree.column("Store", width=200, anchor=tk.CENTER)

        tree.heading("Category", text="カテゴリ")
        tree.column("Category", width=120, anchor=tk.CENTER)

        tree.heading("year", text="Year")
        tree.column("year", width=50, anchor=tk.CENTER)

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
                stores = data[4]
                categorys = data[5]
                years = data[6]
                
                tree.insert('', tk.END, values=[ids, titles, stores, categorys, years])

            # Treeviewの行がクリックされたときのイベントバインド
            def _on_item_click(event):
                item = tree.selection()[0]
                list_id = tree.item(item, 'values')[0]
                _click_detail(event, list_id)

            tree.bind('<ButtonRelease-1>', _on_item_click)

        gui_data(self.result, self.count_all)
        
        root_li.mainloop() 

if __name__ == '__main__':
    list = CatalogList()
    list.list_view()
