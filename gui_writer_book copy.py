import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext 
# リスト表示用ＳＱＬ
# from dbc_writer import Writer
# 個別（詳細）表示用ＳＱＬ
from gui_book_detail import Detail

# gui_wrier_detailからデータを受け取ってＧＵＩを表示する関数を呼ぶ
def list_view_mini(result):
    # リスト表示用のＳＱＬを呼ぶ
    # result = book_list(id)

    # 詳細ボタンクリック
    # IDを元に詳細画面を開く
    def click_detail(event,list_id):
        detail = Detail(list_id)
        detail.gui_detail()
        

    # ＧＵＩの作成  ------------------------------------------------  
    root_li = tk.Toplevel()
    root_li.title('著者別データ')
    root_li.geometry('400x400+1300+100')
    # 背景色
    back_color = '#FFCC66'
    # ボタンの色
    button_color = '#FF9933'
    # テキストボックスの色
    text_back_color = '#FFFFCC'
    root_li.configure(bg=back_color)

    # フレーム
    frame_hed = tk.Frame(root_li, width=380, height=50, pady=5, padx=20)
    frame_hed.configure(bg=back_color)
    # scrollbar------------------
    # canvas（フレームをのせて、スクロールバーを紐付ける）
    canvas_li = tk.Canvas(root_li, width=350,height=300)
    # highlightthickness(操作時に枠線が出ないようにする)
    canvas_li.configure(bg=back_color, highlightthickness=0)
    canvas_li.grid(row=2, column=0)
    # 垂直方向のスクロールバーを作成
    scrollbar = ttk.Scrollbar(root_li,orient=tk.VERTICAL)
    # canvasの右に垂直のスクロールバーを配置
    scrollbar.grid(row=2, column=1, sticky=tk.N + tk.S)
    # スクロールバーが稼働時の処理
    scrollbar.config(command=canvas_li.yview)
    # canvasクロール時の処理
    canvas_li.config(yscrollcommand=scrollbar.set)
    # 下の方にあるscroll_view()関数でcanvas_liにframeを描画する処理とスクロール量の算出を行う    
    #--------------

    # データのリスト表示部分
    frame_body = tk.Frame(canvas_li, width=380,height=300, pady=5, padx=20)
    frame_body.configure(bg=back_color)
    frame_hed.grid(row=0, column=0)
    frame_body.grid(row=2, column=0, sticky=tk.E)

    # 件数表示用
    count_id = tk.Entry(frame_hed, width=6, bg=text_back_color)
    count_id.place(x=20, y=10)

    '''
     リスト表示部分のテキスト（Entry）作成とデータの挿入
     引数は、ＳＱＬの結果（タプル）
     戻り値は、データ件数（数値）
    '''
    def gui_data(result:tuple)->int:
        # 項目ごとにリストにとる
        ids = [data[0] for data in result]
        titles = [data[1] for data in result]
        publishers = [data[7] for data in result]
        # 各リストの中身とインデックスを取得
        for i, (id, title, publisher) in enumerate(zip(ids, titles, publishers)):
            i = i+1
            list_id = id
            # title Entry
            text_list_title = tk.Entry(frame_body, width=20)
            text_list_title.insert(0,title)
            text_list_title.configure(state= 'readonly')
            text_list_title.grid(row=[i], column=0, padx=2, pady=2, sticky=tk.W)
            # publisher Entry
            text_list_publisher = tk.Entry(frame_body, width=20)
            text_list_publisher.insert(0,publisher)
            text_list_publisher.configure(state= 'readonly')
            text_list_publisher.grid(row=[i], column=1, padx=2, pady=2, sticky=tk.W)
            # 詳細ボタン
            # command=click_detailではなく、bindを使うとrow（何行目）が取得できる
            button_detail = tk.Button(frame_body, width=5, height=1, bg=button_color,  text='詳細')
            #<ButtonPress> 左クリックイベント
            # 引数で変数（該当ＩＤ）を渡す
            button_detail.bind("<ButtonPress>", lambda event, arg=list_id: click_detail(event, arg) )
            button_detail.grid(row=[i], column=2, padx=3, pady=2,sticky=tk.W)
        # 件数表示 
        count_i = i 
        count_id.insert(0,f'{count_i}件')
        return count_i

    '''
    widgetの作成とデータの挿入・ボタンの配置 
    初回はここから関数呼ぶ
    並び替え、検索、実行時には、その関数から 呼出だす
    戻り値で件数を受け取る
    '''
    count_i = gui_data(result)

    '''
    データ件数（count_i）を元にスクロール量を算出
    １行を32pxとして、動的にスクロールを変化させる
    （データ件数×32px）－フレームの高さ
    '''    
    def scroll_view(count_i:int):
        #スクロール範囲(1行を34pxとして行数分をスクロールさせる)
        sc_height = (count_i * 38)-300
        #print(sc_height)
        canvas_li.config(scrollregion=(0,0,0,sc_height)) 
        # canvasにframeを描画する    
        canvas_li.create_window((0, 0), window=frame_body, anchor="nw")
    
    # スクロール量を算出する関数にデータ件数を送る
    scroll_view(count_i)
           
    # root_li.mainloop()

if __name__ == '__main__':
    id = 6
    list_view_mini(id)
