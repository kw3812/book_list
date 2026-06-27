import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os
import shutil
import subprocess
from gui_book_list import BookList
from gui_book_insert import gui_insert
from gui_writer_list import WriterList
from gui_writer_insert import writer_insert as gwi
from gui_publisher_list import PublisherList
from gui_publisher_insert import publisher_insert as gpi
from gui_catalog_list import CatalogList
from gui_catalog_insert import gui_insert as gci
from gui_chart import veiw_chart
import book_json 
from  book_list_backup import DataBackup
from ftp import ftp_upload
from def_param import XAMPP_PATH, APP_PATH, UPLOAD_PATH, BACK_COLOR, BUTTON_COLOR, BUTTON_COLOR2, TEXT_COLOR

# ＧＵＩの作成  
root_menu = tk.Tk()
root_menu.title('書籍データ')
root_menu.geometry('500x570+100+100')
#　メニューバー
def click_version():
    messagebox.showinfo('version情報', 'Books_data:version 1.1')
menubar = tk.Menu()
root_menu.config(menu=menubar)
# menubarを親としてヘルプメニューを作成と表示
v_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='menu', menu=v_menu)
# 設定メニューにプルダウンメニューを追加
v_menu.add_command(label='version情報',command = click_version)

# GUI
frame_menu = tk.Frame(root_menu, width=500, height=460, pady=50, padx=60)
frame_menu.configure(bg=BACK_COLOR)
frame_menu.grid(row=0, column=0)

def open_book_list():
    book_list = BookList()
    book_list.list_view()
def open_book_insert():
    gui_insert()
def open_writer_list():
    wl = WriterList()
    wl.list_view()
def open_writer_insert():
    gwi()
def open_publisher_list():
    pl = PublisherList()
    pl.list_view()
def open_publiser_insert():
    gpi()
def open_catalog_list():
    catalog = CatalogList()
    catalog.list_view()   
def open_catalog_insert():
    gci()
def data_backup():
    # json変換
    df_disp = book_json.convert_json('disp_table')
    df_book = book_json.convert_json('book_table')
    book_json.json_write(df_disp, df_book)

    # JSONファイルをコピー
    # アップロード用のフォルダ
    shutil.copy2(f'{APP_PATH}/book.json', f'{UPLOAD_PATH}/book.json')
    # backup
    db = DataBackup()
    db.deta_backup()
    # shinobi.jpにアップロード
    ftp_upload()

def click_end():
    subprocess.Popen(f'{XAMPP_PATH}/apache_stop.bat',shell = True)
    subprocess.Popen(f'{XAMPP_PATH}/mysql_stop.bat',shell = True)

    # プログラム自体の終了
    raise SystemExit

def click_chart():
    veiw_chart()

# title label
label_title = tk.Label(frame_menu, text='BooksData', background=BACK_COLOR, font=('',24), foreground=TEXT_COLOR)
label_title.grid(row=0, column=0, columnspan=2, padx=15, pady=10)
# Button
button_list = tk.Button(frame_menu, width=15, height=2, text='書籍リスト', command=open_book_list ,background=BUTTON_COLOR, font=('',14))
button_list.grid(row=1, column=0,padx=15, pady=10)
button_insert = tk.Button(frame_menu, width=15, height=2, text='本の追加', command=open_book_insert ,background=BUTTON_COLOR, font=('',14))
button_insert.grid(row=1, column=1,padx=15, pady=10)
button_writer_list = tk.Button(frame_menu, width=15, height=2, text='著者リスト', command=open_writer_list, background=BUTTON_COLOR, font=('',14))
button_writer_list.grid(row=3, column=0,padx=15, pady=10)
button_writer_insert = tk.Button(frame_menu, width=15, height=2, text='著者追加', command=open_writer_insert, background=BUTTON_COLOR, font=('',14))
button_writer_insert.grid(row=3, column=1,padx=15, pady=10)
button_publisher_list = tk.Button(frame_menu, width=15, height=2, text='出版社リスト', command=open_publisher_list, background=BUTTON_COLOR, font=('',14))
button_publisher_list.grid(row=5, column=0,padx=15, pady=10)
button_publisher_insert = tk.Button(frame_menu, width=15, height=2, text='出版社追加', command=open_publiser_insert, background=BUTTON_COLOR, font=('',14))
button_publisher_insert.grid(row=5, column=1,padx=15, pady=10)

button_catalog_list = tk.Button(frame_menu, width=15, height=2, text='その他リスト', command=open_catalog_list, background=BUTTON_COLOR, font=('',14))
button_catalog_list.grid(row=7, column=0,padx=15, pady=10)
button_catalog_insert = tk.Button(frame_menu, width=15, height=2, text='その他追加', command=open_catalog_insert, background=BUTTON_COLOR, font=('',14))
button_catalog_insert.grid(row=7, column=1,padx=15, pady=10)

button_end = tk.Button(frame_menu, width=15, height=2, text='グラフ', command=click_chart, background=BUTTON_COLOR, font=('',14))
button_end.grid(row=9, column=0,padx=15, pady=10)
button_backup = tk.Button(frame_menu, width=15, height=2, text='バックアップ', command=data_backup, background=BUTTON_COLOR2, font=('',14))
button_backup.grid(row=10, column=0,padx=15, pady=10)
button_end = tk.Button(frame_menu, width=15, height=2, text='終了', command=click_end, background=BUTTON_COLOR2, font=('',14))
button_end.grid(row=10, column=1,padx=15, pady=10)

# 境界線
line1 = ttk.Separator(frame_menu,orient='horizontal')
line2 = ttk.Separator(frame_menu,orient='horizontal')
line3 = ttk.Separator(frame_menu,orient='horizontal')
line4 = ttk.Separator(frame_menu,orient='horizontal')
line5 = ttk.Separator(frame_menu,orient='horizontal')
line6 = ttk.Separator(frame_menu,orient='horizontal')

line1.grid(row=2, column=0, columnspan=2, sticky="ew")
line2.grid(row=4, column=0, columnspan=2, sticky="ew")
line3.grid(row=6, column=0, columnspan=2, sticky="ew")
line4.grid(row=8, column=0, columnspan=2, sticky="ew")
root_menu.mainloop()