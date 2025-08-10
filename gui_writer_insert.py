import tkinter as tk
import tkinter.ttk as ttk
import re
from tkinter import scrolledtext 
from tkinter import messagebox
from dbc_writer import Writer
from gui_writer_detail import gui_writer_detail
from validate import v_rubi2

def writer_insert():
        # ボタンクリック処理
    def click_insert():
        # エラーを格納するリスト
        err_mes =list()
        # タイトルの未入力をチェック
        writer = text_writer.get()
        if len(writer) == 0:
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
            writer_class = Writer()
            last_id = writer_class.insert(writer,rubi,memo)
            print(last_id)
            # 各項目の初期化（クリア）
            text_rubi.delete(0, tk.END)
            text_writer.delete(0, tk.END)
            text_memo.delete("1.0","end")
            # 生成されたＩＤを元に詳細画面を開く
            gui_writer_detail(last_id[0])
            root_rins.destroy()

        else:
            #　エラーメッセージを表示
            messagebox.showinfo('入力エラー', err_mes)
            
        # ＧＵＩの作成　-----------------------------------------------------
    root_rins = tk.Toplevel()
    root_rins.title('著者データ')
    root_rins.geometry('600x400+610+80')
    # 背景色
    back_color = '#FFCC66'
    # ボタンの色
    button_color = '#FF9933'
    # テキストボックスの色
    text_back_color = '#FFFFCC'
    root_rins.configure(bg=back_color)
    frame_rubi = tk.Frame(root_rins,width=600, height=20, pady=15, padx=20)
    frame_rubi.configure(bg=back_color)
    frame_writer = tk.Frame(root_rins,width=600, height=20, pady=15, padx=10)
    frame_writer.configure(bg=back_color)
    frame_memo = tk.Frame(root_rins,width=600, height=100, pady=15, padx=10)
    frame_memo.configure(bg=back_color)
  # フリガナのlabelとEntry
    '''
    コールバック関数でTrue or Falseを受け取り、Falesの場合入力を不可にする
    Tcl関数  register(Validationの関数)
    '''
    tcl_v_rubi= root_rins.register(v_rubi2)
    label_rubi = tk.Label(frame_rubi, text='フリガナ', background=back_color)
    text_rubi = tk.Entry(frame_rubi, width=70,background=text_back_color, validate='key',vcmd=(tcl_v_rubi, '%S')) 
    label_rubi.pack(side=tk.LEFT)
    text_rubi.pack(side=tk.RIGHT)

# 著者のlabelとEntry
    label_writer = tk.Label(frame_writer, text='著者', background=back_color)
    text_writer = tk.Entry(frame_writer, width=40,background=text_back_color, font=('',16))
    label_writer.pack(side=tk.LEFT)
    text_writer.pack(side=tk.RIGHT)

  # メモ Text
    text_memo = tk.Text(frame_memo,  width=70, height=15,background=text_back_color)
    # memo欄にスクロール（縦）を設置
    scrollbar = tk.Scrollbar(frame_memo, orient=tk.VERTICAL, command=text_memo.yview)
    text_memo["yscrollcommand"] = scrollbar.set
    text_memo.pack(side=tk.LEFT,)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Button
    button_insert = tk.Button(root_rins, width=10, text='追加', command=click_insert, background=button_color)
    
    frame_rubi.pack()
    frame_writer.pack()
    frame_memo.pack()
    button_insert.pack()

    # root_rins.mainloop()

if __name__ == '__main__':
    writer_insert()


