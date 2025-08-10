import subprocess
#from time import sleep

# xammppを開く
# subprocess.Popen(r'D:\xampp\xampp-control.exe',shell = True)
# sleep(1)
subprocess.Popen(r'D:\xampp\apache_start.bat',shell = True)
subprocess.Popen(r'D:\xampp\mysql_start.bat',shell = True)
subprocess.Popen(r'D:\xampp\htdocs\book_list\gui_top_menu.py',shell = True)

