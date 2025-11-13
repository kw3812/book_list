import subprocess
import def_url

class DataBackup:
    def __init__(self):
        # MySQLの設定
        self.mysql_bin_path = f"{def_url.xammp_url}/mysql/bin"
        self.backup_file = f"{def_url.xammp_backup_url}/book_list_bakup.dump"

        
    def deta_backup(self):
        # 実行コマンド（リスト形式で指定するのが安全）
        cmd = [
            "mysqldump",
            "--default-character-set=utf8",
            "--single-transaction",
            "-u", "root",
            "book_list"
        ]

        # 出力ファイルにリダイレクト
        with open(self.backup_file, "w", encoding="utf-8") as f:
            subprocess.run(cmd, cwd=self.mysql_bin_path, stdout=f, stderr=subprocess.PIPE, text=True, shell=True)

    def deta_restore(self):

        # 実行コマンド
        cmd = [
            "mysql",
            "-u", "root",
            "book_list"
        ]

        # 復元実行
        with open(self.backup_file, "r", encoding="utf-8") as f:
            result = subprocess.run(cmd, cwd=self.mysql_bin_path, stdin=f,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, shell=True)
