import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext 
# リスト表示用ＳＱＬ
# from dbc_publisher import Publisher
# 個別（詳細）表示用ＳＱＬ
from gui_book_detail import Detail
from def_param import BACK_COLOR, BUTTON_COLOR, TEXT_BOX_COLOR

class WriterPublisher(tk.Toplevel):
    def __init__(self, parent,result):
        super().__init__(parent)
        self.transient(parent)
        # ＧＵＩの作成  ------------------------------------------------  
        # self = tk.Toplevel()
        self.title('出版社別データ')
        self.geometry('400x400+1300+100')
        self.configure(bg=BACK_COLOR)
        self.result = result

    # 詳細ボタンクリック
    # IDを元に詳細画面を開く
    def _click_detail(event,list_id):
        detail = Detail(list_id)
        detail.gui_detail(list_id)
        

    def list_view_mini2(self):
        # フレーム
        frame_hed = tk.Frame(self, width=380, height=50, pady=5, padx=20)
        frame_hed.configure(bg=BACK_COLOR)
        # scrollbar------------------
        # canvas（フレームをのせて、スクロールバーを紐付ける）
        self.canvas_li = tk.Canvas(self, width=350,height=300)
        # highlightthickness(操作時に枠線が出ないようにする)
        self.canvas_li.configure(bg=BACK_COLOR, highlightthickness=0)
        self.canvas_li.grid(row=2, column=0)
        # 垂直方向のスクロールバーを作成
        scrollbar = ttk.Scrollbar(self,orient=tk.VERTICAL)
        # canvasの右に垂直のスクロールバーを配置
        scrollbar.grid(row=2, column=1, sticky=tk.N + tk.S)
        # スクロールバーが稼働時の処理
        scrollbar.config(command=self.canvas_li.yview)
        # canvasクロール時の処理
        self.canvas_li.config(yscrollcommand=scrollbar.set)
        # 下の方にある_scroll_view()関数でself.canvas_liにframeを描画する処理とスクロール量の算出を行う    
        #--------------

        # データのリスト表示部分
        self.frame_body = tk.Frame(self.canvas_li, width=380,height=300, pady=5, padx=20)
        self.frame_body.configure(bg=BACK_COLOR)
        frame_hed.grid(row=0, column=0)
        self.frame_body.grid(row=2, column=0, sticky=tk.E)

        # 件数表示用
        self.count_id = tk.Entry(frame_hed, width=6, bg=TEXT_BOX_COLOR)
        self.count_id.place(x=20, y=10)

        self.gui_data(self.result)

        '''
        リスト表示部分のテキスト（Entry）作成とデータの挿入
        引数は、ＳＱＬの結果（タプル）
        戻り値は、データ件数（数値）
        '''
    def gui_data(self, result:tuple)->int:
        # 項目ごとにリストにとる
        ids = [data[0] for data in result]
        titles = [data[1] for data in result]
        writers = [data[5] for data in result]
        # 各リストの中身とインデックスを取得
        for i, (id, title, writer) in enumerate(zip(ids, titles, writers)):
            i = i+1
            list_id = id
            # title Entry
            text_list_title = tk.Entry(self.frame_body, width=20)
            text_list_title.insert(0,title)
            text_list_title.configure(state= 'readonly')
            text_list_title.grid(row=[i], column=0, padx=2, pady=2, sticky=tk.W)
            # writer Entry
            text_list_writer = tk.Entry(self.frame_body, width=20)
            text_list_writer.insert(0,writer)
            text_list_writer.configure(state= 'readonly')
            text_list_writer.grid(row=[i], column=1, padx=2, pady=2, sticky=tk.W)
            # 詳細ボタン
            # command=self._click_detailではなく、bindを使うとrow（何行目）が取得できる
            button_detail = tk.Button(self.frame_body, width=5, height=1, bg=BUTTON_COLOR,  text='詳細')
            #<ButtonPress> 左クリックイベント
            # 引数で変数（該当ＩＤ）を渡す
            button_detail.bind("<ButtonPress>", lambda event, arg=list_id: self._click_detail(event, arg) )
            button_detail.grid(row=[i], column=2, padx=3, pady=2,sticky=tk.W)
        # 件数表示 
        count_i = i 
        self.count_id.insert(0,f'{count_i}件')
        # self.スクロール量を算出する関数にデータ件数を送る
        self._scroll_view(count_i)

        '''
        データ件数（count_i）を元にスクロール量を算出
        １行を32pxとして、動的にスクロールを変化させる
        （データ件数×32px）－フレームの高さ
        '''    
    def _scroll_view(self, count_i:int):
        #スクロール範囲(1行を34pxとして行数分をスクロールさせる)
        sc_height = (count_i * 38)-300
        #print(sc_height)
        self.canvas_li.config(scrollregion=(0,0,0,sc_height)) 
        # canvasにframeを描画する    
        self.canvas_li.create_window((0, 0), window=self.frame_body, anchor="nw")
        
            

