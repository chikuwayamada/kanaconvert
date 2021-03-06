#!/usr/bin/env python

import sys
import codecs
import re

# かな変換テーブル
kana_table = {
    'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お',
    'ka': 'か', 'ki': 'き', 'ku': 'く', 'ke': 'け', 'ko': 'こ',
    'sa': 'さ', 'si': 'し', 'su': 'す', 'se': 'せ', 'so': 'そ',
    'ta': 'た', 'ti': 'ち', 'tu': 'つ', 'te': 'て', 'to': 'と',
    'na': 'な', 'ni': 'に', 'nu': 'ぬ', 'ne': 'ね', 'no': 'の',
    'ha': 'は', 'hi': 'ひ', 'hu': 'ふ', 'he': 'へ', 'ho': 'ほ',
    'ma': 'ま', 'mi': 'み', 'mu': 'む', 'me': 'め', 'mo': 'も',
    'ya': 'や', 'yu': 'ゆ', 'yo': 'よ',
    'ra': 'ら', 'ri': 'り', 'ru': 'る', 're': 'れ', 'ro': 'ろ',
    'wa': 'わ',
    'ga': 'が', 'gi': 'ぎ', 'gu': 'ぐ', 'ge': 'げ', 'go': 'ご',
    'za': 'ざ', 'zi': 'じ', 'zu': 'ず', 'ze': 'ぜ', 'zo': 'ぞ',
    'da': 'だ', 'di': 'ぢ', 'du': 'づ', 'de': 'で', 'do': 'ど',
    'ba': 'ば', 'bi': 'び', 'bu': 'ぶ', 'be': 'べ', 'bo': 'ぼ',
    'pa': 'ぱ', 'pi': 'ぴ', 'pu': 'ぷ', 'pe': 'ぺ', 'po': 'ぽ',
    'kya': 'きゃ', 'kyu': 'きゅ', 'kyo': 'きょ',
    'sya': 'しゃ', 'syu': 'しゅ', 'syo': 'しょ',
    'tya': 'ちゃ', 'tyu': 'ちゅ', 'tyo': 'ちょ',
    'nya': 'にゃ', 'nyu': 'にゅ', 'nyo': 'にょ',
    'hya': 'ひゃ', 'hyu': 'ひゅ', 'hyo': 'ひょ',
    'mya': 'みゃ', 'myu': 'みゅ', 'myo': 'みょ',
    'rya': 'りゃ', 'ryu': 'りゅ', 'ryo': 'りょ',
    'gya': 'ぎゃ', 'gyu': 'ぎゅ', 'gyo': 'ぎょ',
    'zya': 'じゃ', 'zyu': 'じゅ', 'zyo': 'じょ',
    'jya': 'じゃ', 'jyu': 'じゅ', 'jyo': 'じょ',
    'bya': 'びゃ', 'byu': 'びゅ', 'byo': 'びょ',
    'pya': 'ぴゃ', 'pyu': 'ぴゅ', 'pyo': 'ぴょ',

    'sha': 'しゃ', 'shi': 'し', 'shu': 'しゅ', 'sho': 'しょ',
    'tsu': 'つ',
    'cha': 'ちゃ', 'chi': 'ち', 'chu': 'ちゅ', 'cho': 'ちょ',
    'fu':'ふ',
    'ja':'じゃ', 'ji':'じ', 'ju':'じゅ', 'jo':'じょ',
    'dya':'ぢゃ', 'dyu':'ぢゅ', 'dyo':'ぢょ',
    'kwa':'くゎ',
    'gwa':'ぐゎ', 'wo':'を',
    'nn' : 'ん',
    '-':'ー', ',':'、', '.':'。',
}

# 母音
boin_list = {
    'a', 'i', 'u', 'e', 'o'
}

# 後ろに来る文字で判断する必要のあるアルファベットのリスト
pend_list = {
    't','n'
}


def searchRomajiStartsWith(romaji):
    # ローマ字のキーを列挙して前方一致。
    # 一致があればTrue
    for k in kana_table.keys():
        if k.startswith(romaji):
            return True
        pass
    pass
    return False


def convertKana(roma_chars):

    # mapにキーのローマ字が存在するかチェック
    if roma_chars in kana_table :
        return kana_table[roma_chars]
    else :
        return False

def convertPendingChars(lastConverted,pendingChar,newChar):
    if pendingChar == 'n':
        # 続く文字が母音でなく直前に変換に成功していれば'ん'
        if newChar not in boin_list and newChar != 'n' and lastConverted:
            return 'ん'
    elif pendingChar == 't':
        # 続く文字が't'で変換に成功していれば'っ'
        if newChar == 't' and lastConverted:
            return 'っ'
        pass
    pass
    return False

def convertRomaJiFile(in_filepath,out_filepath) -> object:
    kanastring = ''

    # ファイルを一行ずつ読み込む
    for line in codecs.open(in_filepath, 'r', 'utf_8'):
        # 全て小文字とする
        line = line.lower()
        out_line = ''
        # 一文字ずつ処理する
        chars = list(line)
        romaji = ''
        # 最終の変換に成功したかどうか
        lastConverted = False
        for char in chars :

            # 後続文字で変化する文字の変換に成功した場合はラインバッファに追加
            pend_char = convertPendingChars(lastConverted,romaji,char)
            if(pend_char != False) :
                out_line += pend_char
                romaji = char
                continue

            # 変換しうる文字かどうかをチェック(変換テーブルのキーと前方一致を取る
            # 対象の文字でない場合、文字バッファをクリアして文字をそのまま結果に代入
            romaji += char
            if(searchRomajiStartsWith(romaji) == False):
                # 判定中の文字バッファがあれば先にラインバッファに移す
                if (romaji != ''):
                    out_line += romaji
                    romaji = ''
                    pass
                lastConverted = False
                continue
            else:
                # アルファベット
                # ローマ字バッファに追加して変換する
                if romaji in pend_list and lastConverted == True:
                    # 後続の文字で変わる文字が入力された場合、変換を待機する
                    lastConverted = True
                    pass
                else :
                    kana = convertKana(romaji)
                    if kana is not False:
                        # 変換成功。カナを行バッファに追加。文字バッファもクリア
                        out_line += kana
                        romaji = ''
                        lastConverted = True
                    else:
                        lastConverted = False
                        # 変換失敗。3文字以上なら変換不能と判断してそのまま行バッファに追加
                        # 1,2文字目なら、なりうる文字か判定。なりえない文字だったらそのまま行バッファに追加
                        mblen = len(romaji)
                        if(mblen >= 3):
                            out_line += romaji
                            romaji = ''
                        pass
                    pass
            pass

        # 未変換のバッファが残っていたら行バッファに追加
        if len(romaji) > 0:
            out_line += romaji
            romaji = ''

        # for debug
        print(out_line)
        kanastring += out_line

    # 変換後のファイルを出力する
    out = codecs.open(out_filepath,'w','utf_8')
    out.write(kanastring)

# 処理スタート
param = sys.argv

# コマンドライン引数が指定どおりになっていなければusageを吐く
if len(param) != 3:
    print('Usage: kanaconvert.py [input_file] [output_file]')
else:
    convertRomaJiFile(param[1], param[2])



