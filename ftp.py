import os
from ftplib import FTP
from def_param import SHINOBI_HOST, SHINOBI_PASS, SHINOBI_USER, UPLOAD_PATH

def ftp_upload():
    # アップロードするローカルのファイルパス
    # 例）D:\\rekisi/walk/stamp
    LOCAL_FILE_PATH = f"{UPLOAD_PATH}/book.json" 
    # サーバー側に保存時のファイルパス
    REMOTE_FILE_NAME = "./stamp/book.json" 

    try:
        # FTPサーバーに接続
        print(f'FTPサーバーに接続中...: {SHINOBI_HOST}')
        with FTP(SHINOBI_HOST) as ftp:
            # ログイン処理
            ftp.login(user=SHINOBI_USER, passwd=SHINOBI_PASS)
            print("ログインに成功しました。")

            # (オプション) 必要に応じてパッシブモードを明示的に有効化
            ftp.set_pasv(True)
            
            # ファイルをバイナリモードでアップロード
            with open(LOCAL_FILE_PATH, "rb") as f:
                # STOR コマンドでファイルを転送
                ftp.storbinary(f"STOR {REMOTE_FILE_NAME}", f)
                
            print(f"アップロード完了: {REMOTE_FILE_NAME}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

def ftp_upload2(images:list):
    # アップロードするローカルのフォルダパス
    LOCAL_FOLDER_PATH = f"{UPLOAD_PATH}/img" 
    # サーバー側に保存時のフォルダパス
    REMOTE_FOLDER_PATH = f"./stamp/img" 

    try:
        # FTPサーバーに接続
        print(f'FTPサーバーに接続中...: {SHINOBI_HOST}')
        with FTP(SHINOBI_HOST) as ftp:
            # ログイン処理
            ftp.login(user=SHINOBI_USER, passwd=SHINOBI_PASS)
            print("ログインに成功しました。")

            # (オプション) 必要に応じてパッシブモードを明示的に有効化
            ftp.set_pasv(True)
            
            for image in images:
                # ローカル画像パス
                LOCAL_FILE_PATH = f'{LOCAL_FOLDER_PATH}/{image}'
                # ファイルをバイナリモードでアップロード
                with open(LOCAL_FILE_PATH, "rb") as f:
                    # STOR コマンドでファイルを転送
                    ftp.storbinary(f"STOR {REMOTE_FOLDER_PATH}/{image}", f)
                    
                print(f"アップロード完了: {image}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    images = ['img1.jpg','img2.jpg']
    ftp_upload()
    # ftp_upload2(images)        