import subprocess
import sys
import def_url

#subprocess.Popen(r'D:\xampp\xampp_stop.exe',shell = True)
subprocess.Popen(f'{def_url.xammp_url}/apache_stop.bat',shell = True)
subprocess.Popen(f'{def_url.xammp_url}/mysql_stop.bat',shell = True)
sys.exit()    
