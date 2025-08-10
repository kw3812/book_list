import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext 
from tkinter import messagebox
# insert SQL
from dbc_catalog import Catalog
from gui_catalog_detail import Detail

def gui_insert():
    # ボタンクリック処理
    def click_insert():
        # タイトルの未入力をチェック
        title = text_title.get()
        event = text_event.get()
        publisher = text_publisher.get()
        store = text_store.get()
        category = text_category.get()
        etc = text_etc.get("1.0", "end")
        year = text_year.get()
        
        catalog = Catalog()
        last_id = catalog.insert(title,event,publisher,store,etc,category,year)
        # 各項目の初期化（クリア）
        text_title.delete(0, tk.END)
        text_event.delete(0, tk.END)
        text_publisher.delete(0, tk.END)
        text_store.delete(0, tk.END)
        text_category.delete(0, tk.END)
        text_etc.delete("1.0","end")
        text_year.delete(0, tk.END)
        # 生成されたＩＤを元に詳細画面を開く
        detail = Detail(last_id[0])
        detail.gui_detail()
        root_ins.destroy()

    # ＧＵＩの作成　-----------------------------------------------------
    #root_ins = tk.Toplevel()
    root_ins = tk.Toplevel()
    root_ins.title('その他書籍データ')
    root_ins.geometry('600x500+610+100')
    # 背景色
    back_color = '#FFCC66'
    # ボタンの色
    button_color = '#FF9933'
    # テキストボックスの色
    text_back_color = '#FFFFCC'
    root_ins.configure(bg=back_color)
    

    # タイトルのlabelとEntry
    label_title = tk.Label(root_ins, text='タイトル', background=back_color)
    label_title.grid(row=1, column=0, sticky=tk.E, padx=5)
    text_title = tk.Entry(root_ins, width=40,background=text_back_color,  font=('',16))
    text_title.grid(row=1, column=1, columnspan=5, sticky=tk.W)
    # イベントのlabelとEntry
    label_event = tk.Label(root_ins, text='イベント', background=back_color)
    label_event.grid(row=2, column=0,sticky=tk.E, padx=3 )
    text_event = tk.Entry(root_ins, width=30,background=text_back_color)
    text_event.grid(row=2, column=1, columnspan=2, sticky=tk.W)
    # 出版社のlabelとEntry
    label_publisher = tk.Label(root_ins,text='出版社', background=back_color)
    label_publisher.grid(row=3, column=2, sticky=tk.E, padx=3)
    text_publisher = tk.Entry(root_ins, width=30,background=text_back_color)
    text_publisher.grid(row=3, column=3,columnspan=2, sticky=tk.W)
    # storeのlabelとEntry
    label_store = tk.Label(root_ins, text='入手先', background=back_color)
    label_store.grid(row=4, column=0,sticky=tk.E, padx=3 )
    text_store = tk.Entry(root_ins, width=30,background=text_back_color)
    text_store.grid(row=4, column=1, columnspan=2, sticky=tk.W)
    # カテゴリのlabelとEntry
    label_category = tk.Label(root_ins, text='カテゴリ', background=back_color)
    label_category.grid(row=5, column=0,sticky=tk.E, padx=3 )
    text_category = tk.Entry(root_ins, width=30,background=text_back_color)
    text_category.grid(row=5, column=1, columnspan=2, sticky=tk.W)
    # yearのlabelとEntry
    label_year = tk.Label(root_ins, text='年', background=back_color)
    label_year.grid(row=5, column=2,sticky=tk.E, padx=3 )
    text_year = tk.Entry(root_ins, width=30,background=text_back_color)
    text_year.grid(row=5, column=3, columnspan=2, sticky=tk.W)
    # メモ Text
    text_etc = tk.Text(root_ins,  width=70, height=15,background=text_back_color)
    # etc欄にスクロール（縦）を設置
    scrollbar = tk.Scrollbar(root_ins, orient=tk.VERTICAL, command=text_etc.yview)
    text_etc["yscrollcommand"] = scrollbar.set
    # etc欄と同位置の右端に設置
    scrollbar.grid(row=6,  column=0, columnspan=4, sticky=(tk.NE, tk.SE))
    text_etc.grid(row=6, column=0, columnspan=4)

    # Button
    button_insert = tk.Button(root_ins, width=10, text='追加', command=click_insert, background=button_color)
    button_insert.grid(row=7, column=3)

    # グリッド割
    root_ins.rowconfigure(0, weight=1)
    root_ins.rowconfigure(1, weight=1)
    root_ins.rowconfigure(2, weight=1)
    root_ins.rowconfigure(3, weight=1)
    root_ins.rowconfigure(4, weight=1)
    root_ins.rowconfigure(5, weight=1)
    root_ins.rowconfigure(6, weight=1)
    root_ins.rowconfigure(7, weight=1)
    root_ins.columnconfigure(0, weight=1)
    root_ins.columnconfigure(1, weight=1)
    root_ins.columnconfigure(2, weight=1)
    root_ins.columnconfigure(3, weight=1)
    root_ins.columnconfigure(4, weight=1)

    root_ins.mainloop()

if __name__ == '__main__':
    gui_insert()

