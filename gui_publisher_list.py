import tkinter as tk
import tkinter.ttk as ttk
from dbc_publisher import Publisher
from gui_publisher_detail import PublisherDtail
from def_param import BACK_COLOR, BUTTON_COLOR, TEXT_BOX_COLOR

class PublisherList:
    def __init__(self):
        sort = 'ID降順'
        # リスト表示用のＳＱＬを呼ぶ
        publisher = Publisher()
        self.result = publisher.list(sort)
        # ＧＵＩの作成  ------------------------------------------------  
        self.root = tk.Toplevel()
        self.root.title('出版社データ')
        self.root.geometry('400x600+610+80')
        self.root.configure(bg=BACK_COLOR)

    def _click_search(self, event):
        input_text = self.seach_text.get()
        publisher = Publisher()
        result = publisher.search(input_text)
        self._gui_data(result)

    def _sort_list(self, event):
        sort = self.combo_sort.get()
        publisher = Publisher()
        result = publisher.list(sort)
        self._gui_data(result)

    def _click_detail(self, event, list_id):
        pd = PublisherDtail(list_id)
        pd.get_publisher_id()

    def _click_clear(self, event):
        self.seach_text.delete(0, tk.END)
        self.combo_sort.delete(0, tk.END)
        self.combo_sort.insert(0, 'ＩＤ降順')
        publisher = Publisher()
        result = publisher.list('ＩＤ降順')
        self._gui_data(result)
    
    # Treeviewにデータを挿入
    def _gui_data(self, result: tuple):
        # Treeviewの既存データをクリア
        self.tree.delete(*self.tree.get_children())
        for i, data in enumerate(result):
            self.tree.insert("", tk.END, values=(data[0], data[1]))
            # 初期データ表示
            # 件数表示 
            count_i = i-1   
            self.count_id.insert(0,f'{count_i}件')

            # self.tree.insert('', tk.END,  values=data)

    # Treeviewの行がクリックされたときのイベントバインド
    def _on_item_click(self, event):
        item = self.tree.selection()[0]
        list_id = self.tree.item(item, 'values')[0]
        self._click_detail(event, list_id)
        # self.tree.bind('<ButtonRelease-1>', self._on_item_click)

    # ＧＵＩの作成  ------------------------------------------------  
    def list_view(self):
        frame_hed = tk.Frame(self.root, width=380, height=100, pady=5, padx=20)
        frame_hed.configure(bg=BACK_COLOR)
        
        # 件数表示用
        self.count_id = tk.Entry(frame_hed, width=6, bg=TEXT_BOX_COLOR, justify="center")
        self.count_id.place(x=20, y=10)

        # ソート用コンボボックス
        sort_value = ('出版社昇順', '出版社降順', 'ＩＤ降順', 'ＩＤ昇順')
        self.combo_sort = ttk.Combobox(frame_hed, width=10, values=sort_value)
        self.combo_sort.place(x=120, y=10)
        self.combo_sort.insert(0, 'ＩＤ降順')
        self.combo_sort.bind('<<ComboboxSelected>>', self._sort_list)

        # 検索用テキスト
        self.seach_text = tk.Entry(frame_hed, width=20, bg=TEXT_BOX_COLOR)
        self.seach_text.place(x=20, y=52)

        # 検索ボタン
        button_search = tk.Button(frame_hed, width=5, bg=BUTTON_COLOR, text='検索')
        button_search.place(x=150, y=50)
        button_search.bind('<ButtonPress>', self._click_search)

        # 解除ボタン
        button_clear = tk.Button(frame_hed, width=5, padx=2, bg=BUTTON_COLOR, text='解除')
        button_clear.place(x=200, y=50)
        button_clear.bind('<ButtonPress>', self._click_clear)

        frame_hed.grid(row=0, column=0)

        # Treeview（テーブル形式のウィジェット）を作成
        columns = ('ID', '出版社')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', height=20)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("",13))
        style.configure("Treeview", background=BACK_COLOR, font=("",13))
        self.tree.bind('<ButtonRelease-1>', self._on_item_click)
        self.tree.column("ID", width=80, minwidth=30, stretch=tk.NO)
        self.tree.column("出版社")
        self.tree.heading('ID', text='ID')
        self.tree.heading('出版社', text='出版社')

        # 垂直スクロールバーを追加
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=1, column=0, sticky='nsew')
        scrollbar.grid(row=1, column=1, sticky='ns')

        self._gui_data(self.result)




        

