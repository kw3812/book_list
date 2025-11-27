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
        case '日本スポーツ企画出版' | '日本スポーツ企画' :
            publisher = '日本スポーツ企画出版社' 
    return publisher     

