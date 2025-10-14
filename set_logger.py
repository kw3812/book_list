import logging
from logging.handlers import TimedRotatingFileHandler


# ログファイル作成
# param logger_name ログの発生元（ファイル名）
# return logger
def get_logger(logger_name:str)->logging.Logger:

    logger = logging.getLogger(logger_name)
    # 出力フォーマット
    formatter = logging.Formatter('[%(levelname)s]  %(asctime)s : %(message)s  (%(filename)s)')
    # レベルをINFO以上に
    logger.setLevel(logging.INFO)
    # 出力先ファイル名
    handler = logging.FileHandler(filename='log.txt', encoding='utf-8')
    # ハンドラーのレベルもINFO以上に
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)	

    return logger

""" 古いログ・ファイルを削除
日付が変わると log.txt.2025-09-20 のようにリネームされて、新しい log.txt が作られる。
backupCount=7 8日目の古いファイルは削除される。
"""
def get_logger2(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    # if not logger.handlers:  # 重複登録防止
    formatter = logging.Formatter(
        '[%(levelname)s]  %(asctime)s : %(message)s  (%(filename)s)'
    )
    logger.setLevel(logging.INFO)

    # 1日ごとにローテーション、7日分残して古いものは削除
    handler = TimedRotatingFileHandler(
        filename='./log/log.txt',
        when='MIDNIGHT',       # 日付が変わるタイミング
        interval=1,     # 1日ごとにローテーション
        backupCount=7,  # 7日分残す（8日目以降は削除）
        encoding='utf-8'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
