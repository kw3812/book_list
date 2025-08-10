import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext 
# ダイアログに使う
from tkinter import messagebox 
# 本の個別表示用ＳＱＬ
# 更新処理用ＳＱＬ  
from dbc_catalog import Catalog

class Detail:
    # 引数は本のＩＤ（数値）
    # tableからIDのデータを読み込む
    def __init__(self, id:int):
        catalog = Catalog()
        self.result = catalog.detail(id)
        # 引数のタプルから、それぞれtkinterの変数にとる
        self.id = self.result[0][0]
        self.title = self.result[0][1]
        self.event = self.result[0][2]
        self.publisher = self.result[0][3]
        self.store = self.result[0][4]
        self.category = self.result[0][5]
        self.etc = self.result[0][6]
        self.year = self.result[0][7]
        self.create_time = self.result[0][8]
        print(self.id, self.title, self.event, self.publisher, self.store, self.category, self.etc, self.year)
    def gui_detail(self):    
        # ＧＵＩの作成
        root_dt = tk.Toplevel()
        root_dt.title('その他データ')
        root_dt.geometry('600x500+810+200')
        # 背景色
        back_color = '#FFCC66'
        # ボタンの色
        button_color = '#FF9933'
        # テキストボックスの色
        text_back_color = '#FFFFCC'
        root_dt.configure(bg=back_color)

        # コンボとスクロールで使うスタイルテーマ
        style_dt = ttk.Style()
        style_dt.theme_use('default')

        ''' 
        他のＧＵＩから呼び出す場合
        textvariableではなくinsertを使う
        stateはconfigureで設定
        '''
        # ID Entry
        text_id = tk.Entry(root_dt, width=6, justify="center")
        text_id.grid(row=0, column=0, sticky=tk.E)
        # タイトル Entry
        text_title = tk.Entry(root_dt, width=90, background=text_back_color ) 
        text_title.grid(row=1, column=0, columnspan=4)
        # event Entry
        label_event = tk.Label(root_dt, text='イベント', background=back_color)
        label_event.grid(row=2, column=0, sticky=tk.E)
        text_event = tk.Entry(root_dt, width=30, background=text_back_color)
        text_event.grid(row=2, column=1, sticky=tk.W)
        # publisher Entry
        label_publisher = tk.Label(root_dt,text='発行', background=back_color)
        label_publisher.grid(row=3, column=0, sticky=tk.E)
        text_publisher = tk.Entry(root_dt, width=30,background=text_back_color)
        text_publisher.grid(row=3, column=1,sticky=tk.W )
        # store Entry
        label_store = tk.Label(root_dt, text='入手場所', background=back_color)
        label_store.grid(row=4, column=0, sticky=tk.E)
        text_store = tk.Entry(root_dt, width=30, background=text_back_color)
        text_store.grid(row=4, column=1, sticky=tk.W)
        # categry Entry
        label_category = tk.Label(root_dt, text='カテゴリ', background=back_color)
        label_category.grid(row=5, column=0, sticky=tk.E)
        text_category = tk.Entry(root_dt, width=30, background=text_back_color)
        text_category.grid(row=5, column=1, sticky=tk.W)
        # year Entry
        label_year = tk.Label(root_dt, text='年', background=back_color)
        label_year.grid(row=5, column=2, sticky=tk.E)
        text_year = tk.Entry(root_dt, width=10, background=text_back_color)
        text_year.grid(row=5, column=3, sticky=tk.W)
        # メモ Text
        text_etc = tk.Text(root_dt,  width=70, height=15, background=text_back_color)
        # etc欄にスクロール（縦）を設置
        style_dt.configure('Vertical.TScrollbar',background=back_color, troughcolor=text_back_color)
        scrollbar = ttk.Scrollbar(root_dt, orient=tk.VERTICAL, command=text_etc.yview)
        text_etc["yscrollcommand"] = scrollbar.set
        # etc欄と同位置の右端に設置
        scrollbar.grid(row=6,  column=0, columnspan=4, sticky=(tk.NE, tk.SE))
        text_etc.grid(row=6, column=0, columnspan=4)

        # データをＧＵＩにセット
        text_id.insert(0,self.id)
        text_id.configure(state= 'readonly')
        text_title.insert(0,self.title)
        if self.event != None:
            text_event.insert(0,self.event)
        if self.publisher != None:
            text_publisher.insert(0,self.publisher)
        if self.store != None:
            text_store.insert(0,self.store)
        if self.category != None:
            text_category.insert(0,self.category)
        text_year.insert(0,self.year)
        if self.etc != None:
            text_etc.insert('1.0',self.etc)

        # 更新ボタンのクリックの処理 --------------------------------------------------
        def _click_update():
            id = text_id.get()
            title = text_title.get()
            event = text_event.get()
            publisher = text_publisher.get()
            store = text_store.get()
            category = text_category.get()
            etc = text_etc.get("1.0", "end")
            year = text_year.get()
            # 更新処理のＳＱＬを呼ぶ
            catalog = Catalog()
            catalog.update(title,event,publisher,store,category,etc,year,id)
            text_title.update()
            text_event.update()
            text_publisher.update()
            text_store.update()
            text_category.update()
            text_etc.update()

        # 削除ボタンのクリック処理  ---------------------------------------
        # dispテーブルにデータを追加して、bookテーブルからは削除
        def _click_delete():
            # 確認メッセージを表示
            del_mes = messagebox.askyesno('警告', '本当に削除ＯＫ？')
            if del_mes == True:
            #     # エラーを格納するリスト
            #     err_mes =list()  
                id = int(text_id.get())
                # 書籍テーブルから削除
                catalog = Catalog()
                catalog.delete(id)
                root_dt.destroy()
            
        # 更新・削除 Button
        button_update = tk.Button(root_dt, width=10, text='更新', command=_click_update ,background=button_color)
        button_update.grid(row=5, column=2,sticky=tk.W)
        button_delete = tk.Button(root_dt, width=10, text='削除', command=_click_delete ,background=button_color)
        button_delete.grid(row=5, column=3,sticky=tk.W)

        root_dt.rowconfigure(0, weight=1)
        root_dt.rowconfigure(1, weight=1)
        root_dt.rowconfigure(2, weight=1)
        root_dt.rowconfigure(3, weight=1)
        root_dt.rowconfigure(4, weight=1)
        root_dt.rowconfigure(5, weight=1)
        root_dt.rowconfigure(6, weight=1)
        # root_dt.rowconfigure(7, weight=1)

        root_dt.columnconfigure(0, weight=1)
        root_dt.columnconfigure(1, weight=1)
        root_dt.columnconfigure(2, weight=1)
        root_dt.columnconfigure(3, weight=1)
        
        root_dt.mainloop()

# 実際にはリスト表示画面から呼ばれる
if __name__ == '__main__':
    detail = Detail(2)
    detail.gui_detail()

