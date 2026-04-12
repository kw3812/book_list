import tkinter as tk
import tkinter.ttk as ttk
import re
from tkinter import scrolledtext 
from tkinter import messagebox
from dbc_publisher import Publisher
from gui_publisher_detail import get_publisher_id
from validate import v_rubi２
from def_param import BACK_COLOR, BUTTON_COLOR, TEXT_BOX_COLOR

def publisher_insert():
        # ボタンクリック処理
    def click_insert():
        # エラーを格納するリスト
        err_mes =list()
        # タイトルの未入力をチェック
        publisher = text_publisher.get()
        if len(publisher) == 0:
            err_mes.append('タイトルを入力してください。\n')
        # フリガナの未入力をチェック    
        rubi = text_rubi.get()
        if len(rubi) == 0:
            err_mes.append('フリガナを入力してください。\n')
        # memoは空白可で、コンボは初期値がある
        memo = text_memo.get("1.0", "end")
        
        '''
        エラーが０だったらデータを書き込むＳＱＬを呼ぶ
        各項目の入力文字をクリア
        ＩＤを元に詳細画面を開く
        エラーがあればメッセージボックスに出力
        '''
        if len(err_mes) == 0:
            # (変数名と変数名の被りに注意)
            publisher_class = Publisher()
            last_id = publisher_class.insert(publisher,rubi,memo)
            # 各項目の初期化（クリア）
            text_rubi.delete(0, tk.END)
            text_publisher.delete(0, tk.END)
            text_memo.delete("1.0","end")
            # 生成されたＩＤを元に詳細画面を開く
            get_publisher_id(last_id[0])
            root_rins.destroy()

        else:
            #　エラーメッセージを表示
            messagebox.showinfo('入力エラー', err_mes)
        # ＧＵＩの作成　-----------------------------------------------------
    root_rins = tk.Toplevel()
    root_rins.title('出版社データ')
    root_rins.geometry('600x400+610+80')
    root_rins.configure(bg=BACK_COLOR)
    frame_rubi = tk.Frame(root_rins,width=600, height=20, pady=15, padx=20)
    frame_rubi.configure(bg=BACK_COLOR)
    frame_publisher = tk.Frame(root_rins,width=600, height=20, pady=15, padx=10)
    frame_publisher.configure(bg=BACK_COLOR)
    frame_memo = tk.Frame(root_rins,width=600, height=100, pady=15, padx=10)
    frame_memo.configure(bg=BACK_COLOR)
  # フリガナのlabelとEntry
    '''
    コールバック関数でTrue or Falseを受け取り、Falesの場合入力を不可にする
    Tcl関数  register(Validationの関数)
    '''
    tcl_v_rubi= root_rins.register(v_rubi2)
    label_rubi = tk.Label(frame_rubi, text='フリガナ', background=BACK_COLOR)
    text_rubi = tk.Entry(frame_rubi, width=70,background=TEXT_BOX_COLOR, validate='key',vcmd=(tcl_v_rubi, '%S')) 
    label_rubi.pack(side=tk.LEFT)
    text_rubi.pack(side=tk.RIGHT)

# 出版社のlabelとEntry
    label_publisher = tk.Label(frame_publisher, text='出版社', background=BACK_COLOR)
    text_publisher = tk.Entry(frame_publisher, width=40,background=TEXT_BOX_COLOR, font=('',16))
    label_publisher.pack(side=tk.LEFT)
    text_publisher.pack(side=tk.RIGHT)

  # メモ Text
    text_memo = tk.Text(frame_memo,  width=70, height=15,background=TEXT_BOX_COLOR)
    # memo欄にスクロール（縦）を設置
    scrollbar = tk.Scrollbar(frame_memo, orient=tk.VERTICAL, command=text_memo.yview)
    text_memo["yscrollcommand"] = scrollbar.set
    text_memo.pack(side=tk.LEFT,)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Button
    button_insert = tk.Button(root_rins, width=10, text='追加', command=click_insert, background=BUTTON_COLOR)
    
    frame_rubi.pack()
    frame_publisher.pack()
    frame_memo.pack()
    button_insert.pack()

    # root_rins.mainloop()

if __name__ == '__main__':
    publisher_insert()


