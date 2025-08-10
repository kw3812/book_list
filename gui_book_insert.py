import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext 
from tkinter import messagebox
# insert SQL
from dbc_book import Book
from gui_book_detail import Detail
from validate import v_rubi
from validate import input_check

def gui_insert():
    # ボタンクリック処理
    def click_insert():
        # エラーを格納するリスト
        err_mes =list()
        # タイトルの未入力をチェック
        title = text_title.get()
        rubi = text_rubi.get()
        writer = text_writer.get()
        publisher = text_publisher.get()
        memo = text_memo.get("1.0", "end")
        state = combo_state.get()
        # 空欄チェック・著者と出版社のＩＤ検索
        err_mes, writer_id, publisher_id = input_check(title, rubi, writer, publisher,state)
        
        '''
        エラーが０だったらデータを書き込むＳＱＬを呼ぶ
        各項目の入力文字をクリア
        ＩＤを元に詳細画面を開く
        エラーがあればメッセージボックスに出力
        '''
        if len(err_mes) == 0:
            book = Book()
            last_id = book.insert(title,rubi,writer_id,publisher_id,memo,state)
            # 各項目の初期化（クリア）
            combo_state.current(0)
            text_rubi.delete(0, tk.END)
            text_title.delete(0, tk.END)
            text_writer.delete(0, tk.END)
            text_publisher.delete(0, tk.END)
            text_memo.delete("1.0","end")
            # 生成されたＩＤを元に詳細画面を開く
            detail = Detail(last_id[0])
            detail.gui_detail()
            root_ins.destroy()

        else:
            #　エラーメッセージを表示
            messagebox.showinfo('入力エラー', err_mes)

    # ＧＵＩの作成　-----------------------------------------------------
    #root_ins = tk.Toplevel()
    root_ins = tk.Toplevel()
    root_ins.title('書籍データ')
    root_ins.geometry('600x400+610+100')
    # 背景色
    back_color = '#FFCC66'
    # ボタンの色
    button_color = '#FF9933'
    # テキストボックスの色
    text_back_color = '#FFFFCC'
    root_ins.configure(bg=back_color)
    

    # state Combobox
    state_value = ('未読', '読書中', '既読')
    combo_state = ttk.Combobox(root_ins,width=10, values= state_value, )
    combo_state.current(0)
    combo_state.grid(row=0, column=3)

    # フリガナのlabelとEntry
    '''
    バリデーション（入力制限）
    importしている v_rubi 関数を呼び出す
    コールバック関数でTrue or Falseを受け取り、Falesの場合入力を不可にする
    Tcl関数  register(Validationの関数)
    '''
    tcl_v_rubi= root_ins.register(v_rubi)
    label_rubi = tk.Label(root_ins, text='フリガナ', background=back_color)
    label_rubi.grid(row=1, column=0, sticky=tk.E, padx=5)
    text_rubi = tk.Entry(root_ins, width=70,background=text_back_color, validate='key',vcmd=(tcl_v_rubi, '%S')) 
    text_rubi.grid(row=1, column=1, columnspan=5, sticky=tk.W)
    # タイトルのlabelとEntry
    label_title = tk.Label(root_ins, text='タイトル', background=back_color)
    label_title.grid(row=2, column=0, sticky=tk.E, padx=5)
    text_title = tk.Entry(root_ins, width=40,background=text_back_color,  font=('',16))
    text_title.grid(row=2, column=1, columnspan=5, sticky=tk.W)
    # 著者のlabelとEntry
    label_writer = tk.Label(root_ins, text='著者', background=back_color)
    label_writer.grid(row=3, column=0,sticky=tk.E, padx=3 )
    text_writer = tk.Entry(root_ins, width=30,background=text_back_color)
    text_writer.grid(row=3, column=1, columnspan=2, sticky=tk.W)
    # 出版社のlabelとEntry
    label_publisher = tk.Label(root_ins,text='出版社', background=back_color)
    label_publisher.grid(row=3, column=2, sticky=tk.E, padx=3)
    text_publisher = tk.Entry(root_ins, width=30,background=text_back_color)
    text_publisher.grid(row=3, column=3,columnspan=2, sticky=tk.W)
    # メモ Text
    text_memo = tk.Text(root_ins,  width=70, height=15,background=text_back_color)
    # memo欄にスクロール（縦）を設置
    scrollbar = tk.Scrollbar(root_ins, orient=tk.VERTICAL, command=text_memo.yview)
    text_memo["yscrollcommand"] = scrollbar.set
    # memo欄と同位置の右端に設置
    scrollbar.grid(row=4,  column=0, columnspan=4, sticky=(tk.NE, tk.SE))
    text_memo.grid(row=4, column=0, columnspan=4)

    # Button
    button_insert = tk.Button(root_ins, width=10, text='追加', command=click_insert, background=button_color)
    button_insert.grid(row=5, column=3)

    # グリッド割
    root_ins.rowconfigure(0, weight=1)
    root_ins.rowconfigure(1, weight=1)
    root_ins.rowconfigure(2, weight=1)
    root_ins.rowconfigure(3, weight=1)
    root_ins.rowconfigure(4, weight=1)
    root_ins.rowconfigure(5, weight=1)
    root_ins.columnconfigure(0, weight=1)
    root_ins.columnconfigure(1, weight=1)
    root_ins.columnconfigure(2, weight=1)
    root_ins.columnconfigure(3, weight=1)
    root_ins.columnconfigure(4, weight=1)

    root_ins.mainloop()

if __name__ == '__main__':
    gui_insert()

