#common
from apps.commons.const import appconst
from apps.commons.util import utils
from apps.commons.bookutil import book_util

#service
from apps.commons.services import service_series   as ss
from apps.commons.services import service_bookInfo as si
from apps.commons.services import service_book     as sb
from apps.commons.services import service_author   as sa

#model
from apps.book.models import Book 
from apps.book.models import Genrue
from apps.book.models import Info
from apps.book.models import Series

"""
編集
"""
# シリーズの取得
def retriveSeries(sereis_id, genrue_id):
    books = Book.objects.filter(series=sereis_id, genrue_id=genrue_id).\
        extra({'volume': "CAST(volume as INTEGER)"}).\
            order_by('read_flg', 'book__sub_title', '-volume')
    return books
# 書籍の取得
def retriveBook(pk):
    book = Book.objects.filter(slug=pk).first()
    return book
# 既読フラグの更新
def updateReadFlg(book):
    b = Book.objects.get(pk=book.file_path)
    b.read_flg = True
    b.save()
# 書籍情報の更新
def book_update(genrue_id, book_id, series_id, book_name, file_path, volume):
    book, updated= Book.objects.update_or_create(
        genrue    = Genrue.objects.get(pk=genrue_id),
        book      = Info.objects.get(pk=book_id),
        series    = Series.objects.get(pk=series_id),
        book_name = book_name,
        file_path = file_path,
        volume    = volume,
    )
# コミット
def commit(book, genrue_id, story_by, art_by, title, sub_title, volume):
    # 拡張子の取得
    extention = utils.getExtention(book.file_path)
    # シリーズの取得
    if genrue_id==appconst.ADULT or genrue_id == appconst.ADULT_NOVEL:
        search = story_by
    else:
        search = title
    series = ss.series_commit(search)
    # 作者の取得
    story_by = sa.author_commit(genrue_id, story_by)
    # 作画の取得
    art_by = sa.author_commit(genrue_id, art_by)
    # 書籍情報の取得
    info = si.info_commit(
        genrue_id, 
        series.series_id, 
        story_by.author_id, 
        art_by.author_id, 
        title, 
        sub_title
    )
    # ジャンル名の取得
    genrue_name = Genrue.objects.get(pk=genrue_id).genrue_name
    # 書籍名の取得
    book_name    = book_util.get_book_name(
        genrue_name, 
        story_by.author_name, 
        art_by.author_name, 
        title, 
        sub_title, 
        volume
    )
    # 保存先
    file_path   = f"{si.savePath(genrue_id)}{book_name}{extention}"
    # 書籍の更新
    sb.book_update(
        genrue_id, 
        info.book_id, 
        series.series_id, 
        book_name, 
        file_path, 
        volume
    )
    # 移動&リネーム
    utils.fileMove(book.file_path, file_path)
    # 古い書籍情報の削除
    book.delete()
def delete(pk):
    book = retriveBook(pk)
    utils.fileDelete(book.file_path)
    book.delete()
"""
要修正一覧
"""
def reviceList():
    # 全書籍の取得
    files = utils.getFiles(appconst.FOLDER_ROOT_BOOK, appconst.EXTENTION_BOOK)
    # 存在しない書籍の整理
    for book in Book.objects.all():
        if not utils.existFile(book.file_path):
            book.delete()
            book.save()
            print(f'【削除】{book.file_path}')
        else:
            try:
                # 存在する要素は削除
                files.remove(book.file_path)
            except Exception as e:
                print(book.file_path)
                print(f'【存在しない】{book.file_path}')
    for file in files:
        utils.fileMove(file, appconst.FOLDER_TORRENT)
    return files
"""
共通
"""
# ジャンルID取得
def getGenrue(series_id):
    book = Book.objects.filter(series_id=series_id).first()
    return book.genrue.genrue_id