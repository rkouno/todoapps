import glob
import os
import re
import shutil
import urllib.parse
import calendar
import requests
from bs4 import BeautifulSoup
from genericpath import isdir, isfile


class utils:
    """
    所定フォルダ以下の特定の拡張子のファイルを取得する
    """
    def getFiles(path, extentions):
        files = []
        for extentoin in extentions:
            files.extend(glob.glob(f'{glob.escape(path)}/**/*.{extentoin}', recursive=True))
        replace_files = [s.replace('\\', '/') for s in files]
        return sorted(set(replace_files))

    """
    所定フォルダ以下のフォルダを取得する
    """
    def getFolders(path, extentions):
        folders = []
        for extention in extentions:
            for folder in glob.glob(f'{glob.escape(path)}/**/*.{extention}', recursive=True):
                folders.append(os.path.dirname(folder))

        return list(set(folders))
    """
    パスからファイル名を取得
    """
    def getFileName(path):
        file_name = os.path.basename(path).replace('\\','/')
        return file_name
        
    """
    拡張子を取得
    """
    def getExtention(file):
        if os.path.isfile(file):
            file, ext = os.path.splitext(file)
            return ext
        return '.pdf'
    """
    正規表現
    """
    def getRegex(text, regex):
        result = ''
        try:
            result = re.search(regex, text).group()
        except Exception as e:
            result = ''
        return result
    """
    正規表現を使って数値のみを取得
    """
    def getVolume(text, regex):
        text = text.translate(str.maketrans({"０": '0', "１": '1', "２": "2", "３": "3", "４": "4", "５": "5", "６": "6", "７": "7", "８": "8", "９": "9"}))
        result = utils.getRegex(text.lower(), regex)
        for volume in re.findall(r'\d+\.\d+|\d+', result):
            if float(volume).is_integer():
                return int(float(volume))
            else:
                return float(volume)
        return 0
    """
    Webスクレイピング
    """
    def WebScraping(url):
        req = requests.get(url)
        html = BeautifulSoup(req.content, 'html.parser')
        return html
    """
    エンコード
    """ 
    def encode(str):
        return urllib.parse.quote(str)
    """
    デコード
    """ 
    def decode(str):
        return urllib.parse.unquote(str)
    """
    ファイルサイズ取得
    """
    def getsize(str):
        return os.path.getsize(str)

    """
    ファイルの存在チェック
    """
    def existFile(file):
        return os.path.isfile(file)
    """
    ファイル判定
    """
    def isFile(path):
        return os.path.isfile(path)
    """
    ファイル削除
    """
    def fileDelete(path):
        if os.path.isfile(path):
            os.remove(path)
    """
    フォルダの存在チェック
    """
    def isDir(path):
        return os.path.isdir(path)
    """
    空フォルダ削除
    """
    def folderEmptyDelete(path):
        for folder in glob.glob(f'{path}/**/', recursive=True):
            try:
                # 空ディレクトリのみ削除（なお子ディレクトリが空になれば親も削除）
                os.removedirs(folder)
                print(f'delete : {folder}')
            except OSError:
                pass
    """
    中身ごとフォルダ削除
    """
    def folder_delete(path):
        shutil.rmtree(path)
    """
    ファイル移動
    """
    def fileMove(before_file, after_dir_or_file):
        after_file = ''
        # 移動元ファイルの存在チェック
        if os.path.isfile(before_file):
            if os.path.isdir(after_dir_or_file):
                # 移動先のパスが存在するフォルダである場合
                after_file = os.path.join(after_dir_or_file, utils.getFileName(before_file))
            else:
                # パスからディレクトリを取得
                dir = os.path.dirname(after_dir_or_file)
                if not os.path.isdir(dir):
                    # ディレクトリが存在しない場合
                    os.makedirs(dir)
                # 移動先のパスがファイルである場合
                after_file = after_dir_or_file
            # 上書きして移動
            shutil.move(before_file, after_file)
    """
    置換（正規表現）
    """
    def replace(txtReplace, txtReplace_b, txtReplace_a):
        return re.sub(txtReplace_b, txtReplace_a, txtReplace)
    
    """
    月末日の取得
    """
    def get_last_date(year, month):
        return f"{year}-{month}-{calendar.monthrange(year, month)[1]}"

    """
    ソートキー
    """
    def atoi(text):
        return int(text) if text.isdigit() else text
    def natural_keys(text):
        return [ utils.atoi(c) for c in re.split(r'(\d+)', text) ]