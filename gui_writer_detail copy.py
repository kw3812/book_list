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
from gui_writer_book import list_view_mini 
# フリガナのバリデーション  
from validate import v_rubi2

# 引数は著者のＩＤ（数値）
# 戻り値はＳＱＬの結果（タプル）
def gui_writer_detail(id:int)->tuple:
    # writer_tableからIDのデータを読み込む
    writer_class = Writer()
    result = writer_class.detail(id)
    w_detail_gui(result)

def w_detail_gui(result):
    # ＧＵＩの作成
    root_wt = tk.Toplevel()
    root_wt.title('著者データ')
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
    writer_id = result[0][0]
    writer = result[0][1]
    writer_rubi = result[0][2]
    memo = result[0][3]
    # ID
    text_id = tk.Entry(frame_id, width=6, justify="center")
    text_id.place(x=10, y=10)
    text_id.insert(0,writer_id)
    text_id.configure(state= 'readonly')
    # rubi
    #フリガナ
    tcl_v_rubi= root_wt.register(v_rubi2) 
    label_rubi = tk.Label(frame_rubi, text='フリガナ', background=back_color)
    text_rubi = tk.Entry(frame_rubi, width=60, background=text_back_color, validate='key',vcmd=(tcl_v_rubi, '%S') ) 
    if writer_rubi != None:
        text_rubi.insert(0,writer_rubi)
    label_rubi.pack(side=tk.LEFT)
    text_rubi.pack(side=tk.RIGHT)
    # 著者
    label_writer = tk.Label(frame_name, text='著者', background=back_color)
    text_writer = tk.Entry(frame_name, width=35, background=text_back_color, font=('',16))
    text_writer.insert(0,writer)
    label_writer.pack(side=tk.LEFT)
    text_writer.pack(side=tk.RIGHT)
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
        writer = text_writer.get()
        memo = text_memo.get("1.0", "end")
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
    def click_delete(): 
        del_mes = messagebox.askyesno('警告', '本当に削除ＯＫ？')
        if del_mes == True:        
            id = int(text_id.get())
            # 書籍テーブルから削除
            writer_class = Writer()
            writer_class.delete(id)
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
    writer_class = Writer()
    result = writer_class.book_list(writer_id)
    # ＳＱＬから返ってきたタプルが空でなければリストを開く
    if len(result) != 0:
        list_view_mini(result)

    # root_wt.mainloop()

if __name__ == '__main__':
    gui_writer_detail(6)



