import glob
import os
import re
import shutil
import urllib.parse

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
            files.extend(glob.glob(f'{path}\*.{extentoin}'))
        return sorted(files)
    """
    所定フォルダ以下のフォルダを取得する
    """
    def getFolders(path):
        folders = [ file_dir for file_dir in glob.glob(f'{path}/**',recursive=True) if os.path.isdir(file_dir) ] 
        return folders
    """
    パスからファイル名を取得
    """
    def getFileName(path):
        file_name = os.path.basename(path)
        return file_name
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
    エンコード
    """ 
    def decode(str):
        return urllib.parse.unquote(str)
    """
    ファイル削除
    """
    def fileDelete(path):
        if os.path.isfile(path):
            os.remove(path)
    """
    フォルダ削除
    """
    def folderDelete(path):
        for folder in glob.glob(f'{path}/**/', recursive=True):
            try:
                # 空ディレクトリのみ削除（なお子ディレクトリが空になれば親も削除）
                os.removedirs(folder)
                print(f'delete : {folder}')
            except OSError:
                pass
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
                if not os.oath.isdir(dir):
                    # ディレクトリが存在しない場合
                    os.makedirs(dir)
                # 移動先のパスがファイルである場合
                after_file = after_dir_or_file
            # 上書きして移動
            shutil.move(before_file, after_file)