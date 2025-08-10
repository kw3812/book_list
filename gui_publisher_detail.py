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
from gui_publisher_book import list_view_mini2
# フリガナのバリデーション  
from validate import v_rubi2

# 引数は著者のＩＤ（数値）
# 戻り値はＳＱＬの結果（タプル）
def get_publisher_id(id:int)->tuple:
    # publisher_tableからIDのデータを読み込む
    publisher_class = Publisher()
    result = publisher_class.detail(id)
    detail_gui(result)

def detail_gui(result):
    
    # ＧＵＩの作成
    root_wt = tk.Toplevel()
    root_wt.title('出版社データ')
    root_wt.geometry('500x470+810+200')
    # 背景色
    back_color = '#FFCC66'
    # ボタンの色
    button_color = '#FF9933'
    # テキストボックスの色
    text_back_color = '#FFFFCC'
    root_wt.configure(bg=back_color)
    frame_id = tk.Frame(root_wt,width=500, height=50, pady=10, padx=20)
    frame_id.configure(bg=back_color)
    frame_rubi = tk.Frame(root_wt,width=500, height=20, pady=15, padx=20)
    frame_rubi.configure(bg=back_color)
    frame_name = tk.Frame(root_wt,width=500, height=20, pady=15, padx=20)
    frame_name.configure(bg=back_color)
    frame_memo = tk.Frame(root_wt,width=500, height=20, pady=15, padx=20)
    frame_memo.configure(bg=back_color)
    frame_footer = tk.Frame(root_wt,width=500, height=20, pady=15, padx=20)
    frame_footer.configure(bg=back_color)

    # 引数のタプルから、それぞれtkinterの変数にとる
    publisher_id = result[0][0]
    publisher = result[0][1]
    publisher_rubi = result[0][2]
    memo = result[0][3]
    # ID
    text_id = tk.Entry(frame_id, width=6, justify="center")
    text_id.place(x=10, y=10)
    text_id.insert(0,publisher_id)
    text_id.configure(state= 'readonly')
    # rubi
    #フリガナ 
    tcl_v_rubi= root_wt.register(v_rubi2) 
    label_rubi = tk.Label(frame_rubi, text='フリガナ', background=back_color)
    text_rubi = tk.Entry(frame_rubi, width=60, background=text_back_color, validate='key',vcmd=(tcl_v_rubi, '%S') ) 
    if publisher_rubi != None:
        text_rubi.insert(0,publisher_rubi)
    label_rubi.pack(side=tk.LEFT)
    text_rubi.pack(side=tk.RIGHT)
    # 出版社
    label_publisher = tk.Label(frame_name, text='出版社', background=back_color)
    text_publisher = tk.Entry(frame_name, width=35, background=text_back_color, font=('',16))
    text_publisher.insert(0,publisher)
    label_publisher.pack(side=tk.LEFT)
    text_publisher.pack(side=tk.RIGHT)
    # メモ Text
    text_memo = tk.Text(frame_memo,  width=60, height=15, background=text_back_color)
    if memo != None:
        text_memo.insert('1.0',memo)
    scrollbar = tk.Scrollbar(frame_memo, orient=tk.VERTICAL, command=text_memo.yview)
    text_memo["yscrollcommand"] = scrollbar.set
    text_memo.pack(side=tk.LEFT,)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # 更新ボタンのクリックの処理
    def click_update():
        # エラーを格納するリスト
        err_mes =list()
        id = int(text_id.get())
        rubi = text_rubi.get()
        publisher = str(text_publisher.get())
        memo = text_memo.get("1.0", "end")
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
    def click_delete():  
        del_mes = messagebox.askyesno('警告', '本当に削除ＯＫ？')
        if del_mes == True:        
            id = int(text_id.get())
            # 書籍テーブルから削除
            publisher_class = Publisher()
            publisher_class.delete(id)
            # ウィンドウを閉じる
            root_wt.destroy()

    # 更新・削除 Button
    button_update = tk.Button(frame_footer, width=10, height=2, text='更新', command=click_update ,background=button_color)
    button_delete = tk.Button(frame_footer, width=10, height=2, text='削除', command=click_delete ,background=button_color)
    button_update.pack(side=tk.LEFT,padx=10)
    button_delete.pack(side=tk.RIGHT,padx=10)

    frame_id.pack()
    frame_rubi.pack()
    frame_name.pack()
    frame_memo.pack()
    frame_footer.pack()

    # 著書の本リストを呼び出す
    publisher_class = Publisher()
    result = publisher_class.book_list(publisher_id)
    # print(type(result))
    # print(result)
    # ＳＱＬから返ってきたタプルが空でなければリストを開く
    if len(result) != 0 :
        list_view_mini2(result)

    # root_wt.mainloop()

if __name__ == '__main__':
   get_publisher_id(1)



