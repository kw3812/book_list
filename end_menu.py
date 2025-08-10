import subprocess
import sys

#subprocess.Popen(r'D:\xampp\xampp_stop.exe',shell = True)
subprocess.Popen(r'D:\xampp\apache_stop.bat',shell = True)
subprocess.Popen(r'D:\xampp\mysql_stop.bat',shell = True)
sys.exit()    
