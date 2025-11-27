import subprocess
from def_path import XAMPP_PATH
#from time import sleep

# xammppを開く
# subprocess.Popen(r'D:\xampp\xampp-control.exe',shell = True)
# sleep(1)
subprocess.Popen(f'{XAMPP_PATH}/apache_start.bat',shell = True)
subprocess.Popen(f'{XAMPP_PATH}/mysql_start.bat',shell = True)

# subprocess.Popen(r'D:\xampp\htdocs\book_list\gui_top_menu.py',shell = True)
