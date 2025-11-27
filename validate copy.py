# 正規表現reの代わりに使う
import regex as re
from tkinter import messagebox
from typing import Tuple
from typing import Union
from dbc_writer import Writer
from dbc_publisher import Publisher
'''
項目の空欄チェックと著者・出版社ＩＤの検索
引数、タイトル・フリガナ・著者・出版社（文字列）
戻り値は、エラーメッセージのリスト・著者ID・出版社ID
'''
# 廃棄書籍データの場合state（項目）がない
def input_check(title:str, rubi:str, writer:str, publisher:str,*state:tuple[str])->tuple[list, int ,int]:
    # 初期化ではなく、ここで宣言しないと使えないローカル変数になる
    writer_id = 0
    publisher_id = 0
    # エラーを格納するリスト
    err_mes =list()
    # タイトルの未入力をチェック
    if len(title) == 0:
        err_mes.append('タイトルを入力してください。\n')
    # フリガナの未入力をチェック    
    if len(rubi) == 0:
        err_mes.append('フリガナを入力してください。\n')
    # 著者のチェック
    # スペースを削除
    writer = re.sub(r"\s+", "", writer)
    if len(writer) == 0:
        err_mes.append('著者を入力してください。\n')
    else:
        # 著者名から著者IDを求めるＳＱＬを呼ぶ
        writer_class = Writer()
        writer_id = writer_class.search_id(writer)
        # 該当がなくＳＱＬからNoneが返ってきた場合
        if not writer_id:
            err_mes.append('データにない著者です。\n')
    # 出版社のチェック        
    if len(publisher) == 0:
        err_mes.append('出版社を入力してください。\n')
    else:
        # 想定される違いを是正する関数を呼ぶ
        publisher = publisher_check(publisher)
        # 出版社名から出版社IDを求めるＳＱＬを呼ぶ
        publisher_class = Publisher()
        publisher_id = publisher_class.search_id(publisher)
        # 該当がなくＳＱＬからNoneが返ってきた場合
        if not publisher_id:
            err_mes.append('データにない出版社です。\n')
    # コンボ（state）
    if len(state) != 0:
        #　可変長引数がタプル
        state = state[0]
        if (state !='未読') and (state != '読書中') and (state != '既読')  :
            err_mes.append('未読・読書中・既読から選択\n')
    return err_mes, writer_id, publisher_id 

'''
書籍テーブル
フリガナのバリデーション
    （ひらがな・半角カタカナ・漢字）はFalseを返す
それ以外はTrueを返す   
''' 
def v_rubi(word:str)->bool:
    # ひらがな
    hiragana = re.compile('[\u3041-\u309F]+')
    # 半角カタカナ
    kana = re.compile('[\uFF66-\uFF9F]+')
    # 漢字
    kanji = re.compile(r'\p{Script=Han}+')
    # 入力文字の判定
    match word:
        case word if hiragana.match(word):
                return False
        case word if kana.match(word):
                return False
        case word if kanji.match(word):
                return False
        case _:
                return True

'''
著者・出版社テーブル
フリガナのバリデーション
全角カタカナ以外はFalseを返す
''' 
def v_rubi2(word:str)->bool:
    # 全角カタカナ
    kana = re.compile('[\u30A1-\u30FF]+')
    # 入力文字の判定
    if kana.match(word):
        return True
    else:
        return False      

''' 
出版社の想定される間違いを是正する関数
引数は入力された出版社名
戻り値も出版社名（修正されなければそのまま）
'''            
def publisher_check(publisher:str)->str:
    match publisher:
        # case publisher if re.search('角川', publisher) :
        #     publisher = 'ＫＡＤＯＫＡＷＡ'
        case 'カドカワ' | 'ｶﾄﾞｶﾜ' | 'KADOKAWA' | '角川' | '角川文庫' | '角川書店':
            publisher = 'ＫＡＤＯＫＡＷＡ' 
        case 'ハルキ文庫' | '角川春樹' :
            publisher = '角川春樹事務所' 
        case '文春文庫' | '文芸春秋' | '文春':
            publisher = '文藝春秋' 
        case '中央公論' | '中央公論社' | '中公文庫' | '中公新書':
            publisher = '中央公論新社' 
        case '光文社文庫' | '光文社新書' :
            publisher = '光文社'
        case '徳間文庫' | '徳間社' | '徳間出版':
            publisher = '徳間書店' 
        case 'ソフトバンク' | 'ＳＯＦＴＢＡＮＫ' | 'softbank' | 'ｓｏｆｔｂａｎｋ' | 'ＳＢクリエイティブ':
            publisher = 'SOFTBANK' 
        case 'ワニ文庫' | 'ワニノベルズ' | 'KKベストセラーズ' | 'kkベストセラーズ' | 'ｋｋベストセラーズ':
            publisher = 'ＫＫベストセラーズ' 
        case '日経ＢＰ' | '日経BP' | '日経' |'日経ナショナルジオグラフィック社' | 'ナショナルジオグラフィック':
            publisher = '日経ＢＰ社' 
        case 'イーストプレス' :
            publisher = 'イースト・プレス' 
        case 'インプレス' | 'インプレス・ジャパン' :
            publisher = 'インプレスジャパン' 
        case 'ハヤカワ文庫' | 'ハヤカワ' | '早川' | '早川文庫':
            publisher = '早川書房' 
        case '都市出版社' | '都市出版株式会社' :
            publisher = '都市出版' 
        case '創元社' | '創元推理文庫' :
            publisher = '東京創元社' 
        case '宝島出版' | '宝島文庫' | '宝島' :
            publisher = '宝島社' 
        case '双葉文庫' | '双葉'  :
            publisher = '双葉社' 
        case '文藝社' | '文庫NEO' | '文芸社文庫' :
            publisher = '文芸社' 
        case 'PHP' | 'php' | 'ｐｈｐ' | 'PHP研究所' | 'ＰＨＰ研究所' :
            publisher = 'ＰＨＰ' 
        case 'NHKブックス' | 'ＮＨＫブックス' | 'NHK' | 'nhk' | 'nhk出版' | 'ＮＨＫ出版' | 'ｎｈｋ出版' | '日本放送出版協会':
            publisher = 'NHK出版' 
        case '朝日新聞出版' | '朝日新聞社'  :
            publisher = '朝日新聞出版社' 
        case '朝日出版' | '朝日文庫'  :
            publisher = '朝日出版社' 
        case '平凡出版' | 'ﾏｶﾞｼﾞﾝﾊｳｽ' :
            publisher = 'マガジンハウス' 
        case 'ワンパブリッシング' | 'ONE PUBLISHING'| 'GetNavi'| 'ゲットナビ編集部' :
            publisher = 'ワン・パブリッシング' 
        case '河出書房' | '河出文庫' | '河出新書' :
            publisher = '河出書房新社' 
    return publisher     

