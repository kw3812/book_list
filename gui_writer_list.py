import tkinter as tk
import tkinter.ttk as ttk
# import re
# リスト表示用ＳＱＬ
# 個別（詳細）表示用ＳＱＬ
# キーワード検索用ＳＱＬ
from dbc_writer import Writer
from gui_writer_detail import gui_writer_detail

# ＳＱＬを受け取ってＧＵＩを表示する関数を呼ぶ
def list_view():
    sort = 'ID降順'
    # リスト表示用のＳＱＬを呼ぶ
    ｗriter = Writer()
    result = ｗriter.list(sort)

    def click_search(event):
        input_text = seach_text.get()
        ｗriter = Writer()
        result = ｗriter.search(input_text)
        gui_data(result)

    def sort_list(event):
        sort = combo_sort.get()
        ｗriter = Writer()
        result = ｗriter.list(sort)
        gui_data(result)

    def click_detail(event, list_id):
        gui_writer_detail(list_id)

    def click_clear(event):
        count_id.delete(0, tk.END)
        seach_text.delete(0, tk.END)
        combo_sort.delete(0, tk.END)
        combo_sort.insert(0, 'ＩＤ降順')
        ｗriter = Writer()
        result = ｗriter.list('ＩＤ降順')
        gui_data(result)

    # ＧＵＩの作成  ------------------------------------------------  
    root_li = tk.Toplevel()
    # root_li = tk.Tk()

    root_li.title('著者リスト')
    root_li.geometry('400x600+610+80')
    back_color = '#FFCC66'
    button_color = '#FF9933'
    text_back_color = '#FFFFCC'
    root_li.configure(bg=back_color)

    frame_hed = tk.Frame(root_li, width=380, height=100, pady=5, padx=20)
    frame_hed.configure(bg=back_color)

    #  件数表示用
    count_id = tk.Entry(frame_hed, width=6, bg=text_back_color, justify="center")
    count_id.place(x=20, y=10)
    
    # sort Combobox
    sort_value = ('著者昇順','著者降順','ＩＤ降順','ＩＤ昇順')
    combo_sort = ttk.Combobox(frame_hed,width=10, values= sort_value )
    combo_sort.place(x=120, y=10)
    combo_sort.insert(0,'ＩＤ降順')
    combo_sort.bind('<<ComboboxSelected>>',  sort_list)

    # 検索用テキスト
    seach_text = tk.Entry(frame_hed, width=20, bg=text_back_color)
    seach_text.place(x=20, y=52)

    # 検索ボタン
    button_search = tk.Button(frame_hed, width=5, bg=button_color, text='検索')
    button_search.place(x=150, y=50)
    #<ButtonPress> 左クリックイベント
    # リストをクリアする関数と、検索関数（ＳＱＬ）を呼ぶ
    button_search.bind("<ButtonPress>", click_search, "+")

    # 解除（初期化）ボタン
    button_clear = tk.Button(frame_hed, width=5, padx=2, bg=button_color, text='解除')
    button_clear.place(x=200, y=50)
    button_clear.bind('<ButtonPress>', click_clear)

    frame_hed.grid(row=0, column=0)

    # Treeview（テーブル形式のウィジェット）を作成
    columns = ('ID', '著者')
    tree = ttk.Treeview(root_li, columns=columns, show='headings', height=20)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("",13))
    style.configure("Treeview", background=back_color, font=("",13))

    tree.heading('ID', text='ID')
    tree.heading('著者', text='著者')

    # 垂直スクロールバーを追加
    scrollbar = ttk.Scrollbar(root_li, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.grid(row=1, column=0, sticky='nsew')
    scrollbar.grid(row=1, column=1, sticky='ns')

    # Treeviewにデータを挿入
    def gui_data(result: tuple):
        # Treeviewの既存データをクリア
        tree.delete(*tree.get_children())
        for i, data in enumerate(result):
            tree.insert("", tk.END, values=(data[0], data[1]))

        # Treeviewの行がクリックされたときのイベントバインド
        def on_item_click(event):
            item = tree.selection()[0]
            list_id = tree.item(item, 'values')[0]
            click_detail(event, list_id)

        tree.bind('<ButtonRelease-1>', on_item_click)

        # 初期データ表示
        # 件数表示 
        count_i = i-1   
        count_id.insert(0,f'{count_i}件')
        return count_i

    count_i = gui_data(result)

    root_li.mainloop() 
       
if __name__ == '__main__':
    list_view()
