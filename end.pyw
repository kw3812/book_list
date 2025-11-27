import subprocess
import sys
from def_path import XAMPP_PATH

#subprocess.Popen(r'D:\xampp\xampp_stop.exe',shell = True)
subprocess.Popen(f'{XAMPP_PATH}/apache_stop.bat',shell = True)
subprocess.Popen(f'{XAMPP_PATH}/mysql_stop.bat',shell = True)
sys.exit()    
