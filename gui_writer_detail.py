import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext 
from tkinter import messagebox 
# 本の個別表示用ＳＱＬ
# 更新処理用ＳＱＬ  
# 著者テーブルから削除するＳＱＬ
# 特定の著者の本リスト（見に行くのはあくまで書籍テーブル）
from dbc_writer import Writer
# 特定の著者の本リスト（ＧＵＩ）
from gui_writer_book import WriterBook 
# フリガナのバリデーション  
from validate import v_rubi2
from def_param import BACK_COLOR, BUTTON_COLOR, TEXT_BOX_COLOR

class WriterDtail:
    def __init__(self, id:int)->tuple:
        # 引数は著者のＩＤ（数値）
        # 戻り値はＳＱＬの結果（タプル）
        # writer_tableからIDのデータを読み込む
        writer_class = Writer()
        result = writer_class.detail(id)
        # ＧＵＩの作成
        self.root = tk.Toplevel()
        self.root.title('著者データ')
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
        self.writer_id = result[0][0]
        writer = result[0][1]
        writer_rubi = result[0][2]
        memo = result[0][3]
        # ID
        self.text_id = tk.Entry(frame_id, width=6, justify="center")
        self.text_id.place(x=10, y=10)
        self.text_id.insert(0,self.writer_id)
        self.text_id.configure(state= 'readonly')
        # rubi
        #フリガナ
        tcl_v_rubi= self.root.register(v_rubi2) 
        label_rubi = tk.Label(frame_rubi, text='フリガナ', background=BACK_COLOR)
        self.text_rubi = tk.Entry(frame_rubi, width=60, background=TEXT_BOX_COLOR, validate='key',vcmd=(tcl_v_rubi, '%S') ) 
        if writer_rubi != None:
            self.text_rubi.insert(0,writer_rubi)
        label_rubi.pack(side=tk.LEFT)
        self.text_rubi.pack(side=tk.RIGHT)
        # 著者
        label_writer = tk.Label(frame_name, text='著者', background=BACK_COLOR)
        self.text_writer = tk.Entry(frame_name, width=35, background=TEXT_BOX_COLOR, font=('',16))
        self.text_writer.insert(0,writer)
        label_writer.pack(side=tk.LEFT)
        self.text_writer.pack(side=tk.RIGHT)
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

    def gui_writer_detail(self):
        # 著書の本リストを呼び出す
        writer_class = Writer()
        result = writer_class.book_list(self.writer_id)
        # ＳＱＬから返ってきたタプルが空でなければリストを開く
        if len(result) != 0:
            wb = WriterBook(self.root, result)
            wb.list_view_mini()

    # 更新ボタンのクリックの処理
    def _click_update(self):
        # エラーを格納するリスト
        err_mes =list()
        id = int(self.text_id.get())
        rubi = self.text_rubi.get()
        writer = self.text_writer.get()
        memo = self.text_memo.get("1.0", "end")
        # タイトルの未入力をチェック
        if len(writer) == 0:
            err_mes.append('タイトルを入力してください。\n')
        # フリガナの未入力をチェック    
        if len(rubi) == 0:
            err_mes.append('フリガナを入力してください。\n')
        if len(err_mes) == 0:
            # # 更新処理のＳＱＬを呼ぶ(変数名と変数名の被りに注意)
            writer_class = Writer()
            writer_class.update(writer,rubi,memo,id)
        else:
            #　エラーメッセージを表示
            messagebox.showinfo('入力エラー', err_mes)
                
    # 削除ボタンのクリック処理
    def _click_delete(self): 
        del_mes = messagebox.askyesno('警告', '本当に削除ＯＫ？')
        if del_mes == True:        
            id = int(self.text_id.get())
            # 書籍テーブルから削除
            writer_class = Writer()
            writer_class.delete(id)
            # ウィンドウを閉じる
            self.root.destroy()






