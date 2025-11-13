import subprocess
import def_url
#from time import sleep

# xammppを開く
# subprocess.Popen(r'D:\xampp\xampp-control.exe',shell = True)
# sleep(1)
subprocess.Popen(f'{def_url.xammp_url}/apache_start.bat',shell = True)
subprocess.Popen(f'{def_url.xammp_url}/mysql_start.bat',shell = True)
# subprocess.Popen(r'D:\xampp\htdocs\book_list\gui_top_menu.py',shell = True)
subprocess.run(["uv", "run", "gui_top_menu.py"], cwd= def_url.book_url,shell = True)


