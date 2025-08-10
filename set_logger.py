import logging

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
