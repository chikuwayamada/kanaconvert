#!/usr/bin/env python

import sys
import re

# 小文字アルファベット正規表現
alpha_pattern = re.compile('[a-z]')

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
    'zya': 'ぢゃ', 'zyu': 'ぢゅ', 'zyo': 'ぢょ',
    'bya': 'びゃ', 'byu': 'びゅ', 'byo': 'びょ',
    'pya': 'ぴゃ', 'pyu': 'ぴゅ', 'pyo': 'ぴょ',

    'sha': 'しゃ', 'shi': 'し', 'shu': 'しゅ', 'sho': 'しょ',
    'tsu': 'つ',
    'cha': 'ちゃ', 'chi': 'ち', 'chu': 'ちゅ', 'cho': 'ちょ',
    'fu':'ふ',
    'ja':'じゃ', 'ji':'じ', 'ju':'じゅ', 'jo':'じょ',
    'dya':'ぢゃ', 'dyu':'ぢゅ', 'dyo':'ぢょ',
    'kwa':'くゎ',
    'gwa':'ぐゎ', 'wo':'を'
}

def convertKana(roma_chars):

    # mapにキーのローマ字が存在するかチェック
    if roma_chars in kana_table :
        return kana_table[roma_chars]
    else :
        return False;


def convertRomaJiFile(in_filepath,out_filepath) -> object:
    kanastring = ''

    # ファイルを一行ずつ読み込む
    for line in open(in_filepath, 'r'):
        # 全て小文字とする
        line = line.lower()
        out_line = ''
        # 一文字ずつ処理する
        chars = list(line)
        romaji = ''
        for char in chars :
            # アルファベットかチェック。
            # アルファベットで無い場合、文字バッファをクリアして文字をそのまま結果に代入
            if(alpha_pattern.match(char) is None):
                # アルファベットでは無いので文字をそのまま行バッファに追加する

                # 判定中の文字バッファがあれば先にラインバッファに移す
                if(romaji != '') :
                    out_line += romaji
                    romaji = ''

                out_line += char

                continue
            else:
                # アルファベット
                # ローマ字バッファに追加して変換する
                # TODO 促音、長音の処理
                romaji += char
                kana = convertKana(romaji)
                if kana is not False:
                    # 変換成功。カナを行バッファに追加。文字バッファもクリア
                    out_line += kana
                    romaji = ''
                else:
                    # 変換失敗。3文字以上なら変換不能と判断してそのまま行バッファに追加
                    if(len(romaji) >= 3) :
                        out_line += romaji
                        romaji = ''
                    pass
                pass
            pass
        print(out_line)
    # 変換後のファイルを出力する
#    out = open(out_filepath,'w')
#    out.write(kanastring)

# main process
param = sys.argv

# コマンドライン引数が指定どおりになっていなければusageを吐く
if len(param) != 3:
    print('Usage: kanaconvert [input_file] [output_file]')
else:
    convertRomaJiFile(param[1], param[2])



