
import os
import socket

from config.settings.base import BASE_DIR


class appconst:
    """
    nyaa 
    """
    # nyaa book RSS
    BOOK_URL            = 'https://nyaa.si/?page=rss&c=3_3'
    BOOK_SEARCH_URL     = 'https://nyaa.si/?page=rss&q=%s&c=3_3&f=0'
    # nyaa anime RSS
    ANIME_URL           = 'https://nyaa.si/?page=rss&q=%s&c=1_4&f=0'
    # nyaa sukebei RSS
    SUKEBEI_URL         = 'https://sukebei.nyaa.si/?page=rss&c=1_4&f=0'
    SUKEBEI_SEARCH_URL  = 'https://sukebei.nyaa.si/?page=rss&q=%s&c=1_4&f=0'
    # dwonload link
    BOOK_DL_URL         = '.*https://nyaa.si/download/.*'
    ADULT_DL_URL        = '.*https://sukebei.nyaa.si/download/.*'

    """
    IIS プロトコル 
    """
    PROTCOL     = "http://"
    IP_ADDRESS  = socket.gethostbyname(socket.gethostname())
    VIDEO_URL   = PROTCOL + IP_ADDRESS + '/Video/'
    TORRENT_URL = PROTCOL + IP_ADDRESS + '/Torrent/'
    MEDIA_URL   = PROTCOL + IP_ADDRESS + ':8080/'

    """
    ディレクトリ
    """
    FOLDER_TORRENT  = 'C:/Torrent/'
    FOLDER_DOWNLOAD = 'D:/download/'
    FOLDER_TODOAPPS = 'D:/todoapps/'
    FOLDER_BASE     = BASE_DIR
    FOLDER_STATIC   = os.path.join(BASE_DIR, 'static/').replace('\\', '/')
    FOLDER_MEDIA    = os.path.join(FOLDER_STATIC, 'media/')

    FOLDER_ROOT_BOOK        = os.path.join(FOLDER_STATIC, 'book/')
    FOLDER_BOOK_ADULT       = os.path.join(FOLDER_ROOT_BOOK, 'adult/')
    FOLDER_BOOK_ADULT_NOVEL = os.path.join(FOLDER_ROOT_BOOK, 'adult_novel/')
    FOLDER_BOOK_COMIC       = os.path.join(FOLDER_ROOT_BOOK, 'comic/')
    FOLDER_BOOK_NOVEL       = os.path.join(FOLDER_ROOT_BOOK, 'novel/')

    FOLDER_MEDIA            = os.path.join(FOLDER_STATIC, 'media/')
    FOLDER_ROOT_UNWATCH     = os.path.join(FOLDER_MEDIA,'unwatch/')
    FOLDER_UNWATCH_VIDEO    = os.path.join(FOLDER_ROOT_UNWATCH,'video/')
    FOLDER_UNWATCH_HENTAI   = os.path.join(FOLDER_ROOT_UNWATCH,'hentai/')
    FOLDER_ROOT_WATCHED     = os.path.join(FOLDER_MEDIA,'watched/')
    FOLDER_WATCHED_VIDEO    = os.path.join(FOLDER_ROOT_WATCHED, 'video/')
    FOLDER_WATCHED_HENTAI   = os.path.join(FOLDER_ROOT_WATCHED, 'hentai/')

    """
    拡張子
    """
    EXTENTION_IMAGE = ("png", "PNG", "jpeg", "jpg", "JPG")
    EXTENTION_BOOK  = ("pdf", "epub")
    EXTENTION_VIDEO = ("mp4", "mkv")
    EXTENTION_ZIP   = ("zip", "rar")

    """
    正規表現
    """
    REGEX_GENRUE                = "(\(一般小説\)|\(一般コミック\)|\(成年コミック\)|\(Novel\)|\(コミック\)|\(Mange\))"
    REGEX_AUTHOR                = "\[.+?\]|【.+?】"
    REGEX_AUTHOR_NONE_BRACKETS  = "(?<=\[).*?(?=\])|(?<=\【).*?(?=\】)"
    REGEX_NUM                   = "\d+.\d+|\d+"
    REGEX_VOLUME                = r"v\d+.\d+|第\d+.\d+巻|v\d+|第\d+巻|\d+.\d+|\d+"
    REGEX_BRACKETS              = "\[.*\] | \(.*\)|\[.*\].| "

    """
    定数
    """
    COMIC       = 1
    NOVEL       = 2
    ADULT       = 3
    ADULT_NOVEL = 4
    # 8MB ずつ読み込む
    chunksize   = 8 * (1024 ** 2)

    """
    タグ
    """
    HENTAI  = 'hentai'
    VIDEO   = 'video'

    """
    ソートコード
    """
    SORT_RECENT = 0
    SORT_TITLE  = 1
    SHOW_ALL    = 2

class template:
    """
    Anime
    """
    ANIME_LIST = 'anime/anime_index.html'
    ANIME_EDIT  = 'anime/anime_edit.html'
    """
    BOOK
    """
    BOOK_CREATE = 'book/book_create.html'
    BOOK_EDIT   = 'book/book_edit.html'
    """
    DOWNLOAD
    """
    NYAA_LIST   = 'download/nyaa_list.html'
    SUKEBEI_LIST= 'download/sukebei_list.html'
    """
    HOME
    """
    HOME_INDEX  = 'home/home_index.html'
    """
    LIBRARY
    """
    BOOK_LIST   = 'library/book_list.html'
    BOOL_REVICE = 'libraty/book_revice.html'
    """
    MASTER
    """
    ADULT_LIST  = 'master/adult_list.html'
    ADULT_EDIT  = 'master/adult_edit.html'
    AUTHOR_LIST = 'master/author_list.html'
    AUTHOR_EDIT = 'master/author_edit.html'
    INFO_LIST   = 'master/info_list.html'
    INFO_EDIT   = 'master/info_edit.html'
    SERIES_LIST = 'master/series_list.html'
    SERIES_EDIT = 'master/series_edit.html'
    """
    VIDEO
    """
    VIDEO_INDEX = 'video/video_index.html'
    VIDEO_WATCH = 'video/video_watch.html'
