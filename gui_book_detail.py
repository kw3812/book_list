import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext 
# ダイアログに使う
from tkinter import messagebox 
# 本の個別表示用ＳＱＬ
# 更新処理用ＳＱＬ  
from dbc_book import Book
# 廃棄書籍テーブルに追加するＳＱＬ
from dbc_disp import Disp
# フリガナとバリデーション  
from validate import v_rubi
# 空欄チェクなど
from validate import input_check

class Detail:
    # 引数は本のＩＤ（数値）
    # book_tableからIDのデータを読み込む
    def __init__(self, id:int):
        book = Book()
        self.result = book.detail(id)
        # 引数のタプルから、それぞれtkinterの変数にとる
        self.book_id = self.result[0][0]
        self.book_title = self.result[0][1]
        self.book_rubi = self.result[0][2]
        self.writer_id = self.result[0][3]
        self.writer = self.result[0][4]
        self.publisher_id = self.result[0][5]
        self.publisher = self.result[0][6]
        self.memo = self.result[0][7]
        self.book_state = self.result[0][8]
        self.create_time = self.result[0][9]

    def gui_detail(self):    
        # ＧＵＩの作成
        root_dt = tk.Toplevel()
        root_dt.title('書籍データ')
        root_dt.geometry('600x400+810+200')
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
        # state Combobox
        style_dt.configure('default.TCombobox',fieldbackground=text_back_color)
        state_value = ('未読', '読書中', '既読')
        combo_state = ttk.Combobox(root_dt,width=10, values= state_value, style='default.TCombobox')
        combo_state.grid(row=0, column=3)
        # タイトル・フリガナ Entry
        tcl_v_rubi= root_dt.register(v_rubi)
        text_rubi = tk.Entry(root_dt, width=70, background=text_back_color, validate='key',vcmd=(tcl_v_rubi, '%S')  ) 
        text_rubi.grid(row=1, column=0, columnspan=4)
        text_title = tk.Entry(root_dt, width=40, background=text_back_color, font=('',16))
        text_title.grid(row=2, column=0, columnspan=4)
        # 著者 Entry
        label_writer = tk.Label(root_dt, text='著者', background=back_color)
        label_writer.grid(row=3, column=0, sticky=tk.E)
        text_writer = tk.Entry(root_dt, width=30, background=text_back_color)
        text_writer.grid(row=3, column=1, sticky=tk.W)
        # 出版社 Entry
        label_publisher = tk.Label(root_dt,text='出版社', background=back_color)
        label_publisher.grid(row=3, column=2, sticky=tk.E)
        text_publisher = tk.Entry(root_dt, width=30,background=text_back_color)
        text_publisher.grid(row=3, column=3,sticky=tk.W )
        # メモ Text
        text_memo = tk.Text(root_dt,  width=70, height=15, background=text_back_color)
        # memo欄にスクロール（縦）を設置
        style_dt.configure('Vertical.TScrollbar',background=back_color, troughcolor=text_back_color)
        scrollbar = ttk.Scrollbar(root_dt, orient=tk.VERTICAL, command=text_memo.yview)
        text_memo["yscrollcommand"] = scrollbar.set
        # memo欄と同位置の右端に設置
        scrollbar.grid(row=4,  column=0, columnspan=4, sticky=(tk.NE, tk.SE))
        text_memo.grid(row=4, column=0, columnspan=4)
        # データをＧＵＩにセット
        text_id.insert(0,self.book_id)
        text_id.configure(state= 'readonly')
        combo_state.insert(0,self.book_state)
        if self.book_rubi != None:
            text_rubi.insert(0,self.book_rubi)
        text_title.insert(0,self.book_title)
        text_writer.insert(0,self.writer)
        text_publisher.insert(0,self.publisher)
        if self.memo != None:
            text_memo.insert('1.0',self.memo)

        # 更新ボタンのクリックの処理 --------------------------------------------------
        def _click_update():
            # エラーを格納するリスト
            err_mes =list()
            id = text_id.get()
            title = text_title.get()
            rubi = text_rubi.get()
            writer = text_writer.get()
            publisher = text_publisher.get()
            memo = text_memo.get("1.0", "end")
            state = combo_state.get()
            err_mes, writer_id, publisher_id = input_check(title, rubi, writer, publisher,state)

            '''
            エラーが０だったらデータを書き込むＳＱＬを呼ぶ
            エラーがあればメッセージボックスに出力
            '''
            if len(err_mes) == 0:
                # 更新処理のＳＱＬを呼ぶ
                book = Book()
                book.update(title,rubi,writer_id,publisher_id,memo,state,id)
                combo_state.update()
                text_rubi.update()
                text_title.update()
                text_writer.update()
                text_publisher.update()
                text_memo.update()
            else:
                #　エラーメッセージを表示
                messagebox.showinfo('入力エラー', err_mes)

        # 削除ボタンのクリック処理  ---------------------------------------
        # dispテーブルにデータを追加して、bookテーブルからは削除
        def _click_delete():
            # 確認メッセージを表示
            del_mes = messagebox.askyesno('警告', '本当に削除ＯＫ？')
            if del_mes == True:
            #     # エラーを格納するリスト
            #     err_mes =list()  
                id = int(text_id.get())
                # 廃棄テーブルに追加
                disp = Disp()
                disp.insert(self.book_title, self.book_rubi, self.writer_id, self.publisher_id, self.memo, self.create_time)
                # 書籍テーブルから削除
                book = Book()
                book.delete(id, self.book_title)
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
        root_dt.columnconfigure(0, weight=1)
        root_dt.columnconfigure(1, weight=1)
        root_dt.columnconfigure(2, weight=1)
        root_dt.columnconfigure(3, weight=1)
        
        root_dt.mainloop()

# 実際にはリスト表示画面から呼ばれる
if __name__ == '__main__':
    detail = Detail(600)
    detail.gui_detail()

