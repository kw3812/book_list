import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.optionxform = str  # 大文字小文字を区別
config.read("def_param.ini", encoding="utf-8")

# PATH  ##################
BASE_DIR = Path(__file__).resolve().parent
# アプリフォルダ
APP_PATH = BASE_DIR 
# XAMPPフォルダ
XAMPP_PATH = BASE_DIR.parent.parent
# バックアップ
BACKUP_PATH = config["PATH"]["BACKUP_PATH"]
# 画像読み込みフォルダ
UPLOAD_PATH = config["PATH"]["UPLOAD_PATH"]
# 画像読み込みフォルダ
SHINOBI_HOST = config["PATH"]["SHINOBI_HOST"]
SHINOBI_USER = config["PATH"]["SHINOBI_USER"]
SHINOBI_PATH = config["PATH"]["SHINOBI_PATH"]

# GUI COLOR  #############
BACK_COLOR = config["GUI"]["BACK_COLOR"]
TEXT_COLOR = config["GUI"]["TEXT_COLOR"]
BUTTON_COLOR = config["GUI"]["BUTTON_COLOR"]
BUTTON_COLOR2 = config["GUI"]["BUTTON_COLOR2"]
TEXT_BOX_COLOR = config["GUI"]["TEXT_BOX_COLOR"]
