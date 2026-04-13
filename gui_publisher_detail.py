import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext 
from tkinter import messagebox 
# 本の個別表示用ＳＱＬ
# 更新処理用ＳＱＬ  
# 書籍テーブルから削除するＳＱＬ
# 特定出版社の本のリスト（ＳＱＬ） 
from dbc_publisher import Publisher
# 特定出版社の本のリスト （ＧＵＩ）
from gui_publisher_book import WriterPublisher
# フリガナのバリデーション  
from validate import v_rubi2
from def_param import BACK_COLOR, BUTTON_COLOR, TEXT_BOX_COLOR

class PublisherDtail:
    def __init__(self, id:int)->tuple:
        publisher_class = Publisher()
        self.result = publisher_class.detail(id)

    # 更新ボタンのクリックの処理
    def _click_update(self):
        # エラーを格納するリスト
        err_mes =list()
        id = int(self.text_id.get())
        rubi = self.text_rubi.get()
        publisher = str(self.text_publisher.get())
        memo = self.text_memo.get("1.0", "end")
        # タイトルの未入力をチェック
        if len(publisher) == 0:
            err_mes.append('タイトルを入力してください。\n')
        # フリガナの未入力をチェック    
        if len(rubi) == 0:
            err_mes.append('フリガナを入力してください。\n')
        if len(err_mes) == 0:
            # 更新処理のＳＱＬを呼ぶ(変数名と変数名の被りに注意)
            publisher_class = Publisher()
            publisher_class.update(publisher,rubi,memo,id)
        else:
            #　エラーメッセージを表示
            messagebox.showinfo('入力エラー', err_mes)

    # 削除ボタンのクリック処理
    def _click_delete(self):  
        del_mes = messagebox.askyesno('警告', '本当に削除ＯＫ？')
        if del_mes == True:        
            id = int(self.self.text_id.get())
            # 書籍テーブルから削除
            publisher_class = Publisher()
            publisher_class.delete(id)
            # ウィンドウを閉じる
            self.root.destroy()

    # 引数は著者のＩＤ（数値）
    # 戻り値はＳＱＬの結果（タプル）
    def get_publisher_id(self):
        # ＧＵＩの作成
        self.root = tk.Toplevel()
        self.root.title('出版社データ')
        self.root.geometry('500x470+810+200')
        self.root.configure(bg=BACK_COLOR)
        frame_id = tk.Frame(self.root,width=500, height=50, pady=10, padx=20)
        frame_id.configure(bg=BACK_COLOR)
        frame_rubi = tk.Frame(self.root,width=500, height=20, pady=15, padx=20)
        frame_rubi.configure(bg=BACK_COLOR)
        frame_name = tk.Frame(self.root,width=500, height=20, pady=15, padx=20)
        frame_name.configure(bg=BACK_COLOR)
        frame_memo = tk.Frame(self.root,width=500, height=20, pady=15, padx=20)
        frame_memo.configure(bg=BACK_COLOR)
        frame_footer = tk.Frame(self.root,width=500, height=20, pady=15, padx=20)
        frame_footer.configure(bg=BACK_COLOR)

        # 引数のタプルから、それぞれtkinterの変数にとる
        publisher_id = self.result[0][0]
        publisher = self.result[0][1]
        publisher_rubi = self.result[0][2]
        memo = self.result[0][3]
        # ID
        self.text_id = tk.Entry(frame_id, width=6, justify="center")
        self.text_id.place(x=10, y=10)
        self.text_id.insert(0,publisher_id)
        self.text_id.configure(state= 'readonly')
        # rubi
        #フリガナ 
        tcl_v_rubi= self.root.register(v_rubi2) 
        label_rubi = tk.Label(frame_rubi, text='フリガナ', background=BACK_COLOR)
        self.text_rubi = tk.Entry(frame_rubi, width=60, background=TEXT_BOX_COLOR, validate='key',vcmd=(tcl_v_rubi, '%S') ) 
        if publisher_rubi != None:
            self.text_rubi.insert(0,publisher_rubi)
        label_rubi.pack(side=tk.LEFT)
        self.text_rubi.pack(side=tk.RIGHT)
        # 出版社
        label_publisher = tk.Label(frame_name, text='出版社', background=BACK_COLOR)
        self.text_publisher = tk.Entry(frame_name, width=35, background=TEXT_BOX_COLOR, font=('',16))
        self.text_publisher.insert(0,publisher)
        label_publisher.pack(side=tk.LEFT)
        self.text_publisher.pack(side=tk.RIGHT)
        # メモ Text
        self.text_memo = tk.Text(frame_memo,  width=60, height=15, background=TEXT_BOX_COLOR)
        if memo != None:
            self.text_memo.insert('1.0',memo)
        scrollbar = tk.Scrollbar(frame_memo, orient=tk.VERTICAL, command=self.text_memo.yview)
        self.text_memo["yscrollcommand"] = scrollbar.set
        self.text_memo.pack(side=tk.LEFT,)
        scrollbar.pack(side=tk.RIGHT, fill="y")


        # 更新・削除 Button
        button_update = tk.Button(frame_footer, width=10, height=2, text='更新', command=self._click_update ,background=BUTTON_COLOR)
        button_delete = tk.Button(frame_footer, width=10, height=2, text='削除', command=self._click_delete ,background=BUTTON_COLOR)
        button_update.pack(side=tk.LEFT,padx=10)
        button_delete.pack(side=tk.RIGHT,padx=10)

        frame_id.pack()
        frame_rubi.pack()
        frame_name.pack()
        frame_memo.pack()
        frame_footer.pack()

        # 著書の本リストを呼び出す
        publisher_class = Publisher()
        self.result = publisher_class.book_list(publisher_id)
        # print(type(self.result))
        # print(self.result)
        # ＳＱＬから返ってきたタプルが空でなければリストを開く
        if len(self.result) != 0 :
            wp = WriterPublisher(self.root, self.result)
            wp.list_view_mini2()




