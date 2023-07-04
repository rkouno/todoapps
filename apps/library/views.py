# util
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages

#common
from apps.commons.const import appconst
from apps.commons.util import utils

#from
from apps.book.froms import BookForm
from apps.master.forms import SeriesForm

#service
from apps.commons.services import service_series   as ss
from apps.commons.services import service_bookInfo as si
from apps.commons.services import service_book     as sb
from apps.commons.services import service_torrent  as st

#download
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

# Create your views here.
"""
書籍一覧
"""
#一覧(一般)
def book_general(request, sort):
    # 検索条件設定
    if 'search' in request.POST:
        request.session['cbxStatus'] = request.POST.get('cbxStatus')
        request.session['txtSearch'] = request.POST['txtSearch']
    cbxStatus = request.session.get('cbxStatus', 0)
    search    = request.session.get('txtSearch', '')
    # ソートモード設定
    request.session['sort'] = sort
    # データ取得
    model = ss.retriveGeneral(search, sort, cbxStatus)
    # ページネーション設定
    models = pagenation(request, model)
    # パラメーター設定
    paramKey = 'books'
    params = {'models' : models, 'alias' : paramKey}

    return render(request, 'library/book_list.html', params)
#一覧(成年)
def book_hentai(request, sort):
    # 検索条件設定
    if 'search' in request.POST:
        request.session['txtSearch']=request.POST['txtSearch']
    search = request.session.get('txtSearch')
    # ソートモード設定
    request.session['sort'] = sort
    # データ取得
    model = ss.retriveHentai(search, sort)
    # ページネーション設定
    models = pagenation(request, model)
    # パラメーター設定    
    paramKey = 'author'
    params = {'models' : models, 'alias' : paramKey}

    return render(request, 'library/book_list.html', params)
"""
シリーズ一覧
"""
#シリーズ一覧(コミック・小説)
def book_series(request, slug):
    series    = ss.getObject(slug)
    genrue_id = si.getSeriesToGenrueId(series.series_name)
    comics    = sb.retriveSeries(series.series_name, appconst.COMIC)
    novels    = sb.retriveSeries(series.series_name, appconst.NOVEL)
    adults    = sb.retriveSeries(series.series_name, appconst.ADULT)

    # ダウンロードリストを更新
    if genrue_id <= appconst.NOVEL:
        st.scraping(series.nyaa_keyword, appconst.BOOK_SEARCH_URL, appconst.BOOK_DL_URL, series)
    else:
        st.scraping(series.nyaa_keyword, appconst.SUKEBEI_SEARCH_URL, appconst.ADULT_DL_URL, series)
    # ダウンロードリストを取得
    torrents = st.downloadList(series.series_name)
    
    # ページネーション設定
    comics   = pagenation(request, comics, 'comic')
    novels   = pagenation(request, novels, 'novel')
    adults   = pagenation(request, adults, 'adult')
    torrents = pagenation(request, torrents, 'torrent')
    # パラメーター設定
    params = {'series' : series,
              'comics'   : comics,
              'novels'   : novels,
              'adults'   : adults,
              'alias'    : 'series', 
              'back'     : 'general', 
              'torrents' : torrents}
    return render(request, 'library/book_list.html', params)

#シリーズ一覧(成年コミック・成年小説)
def book_series_author(request, slug):
    # データ取得
    books = sb.retriveSeries(slug, appconst.ADULT)
    # ページネーション設定
    models = pagenation(request, books)
    # パラメーター設定
    params = {'models' : models, 'alias' : 'series', 'back' : 'hentai'}
    return render(request, 'library/book_list.html', params)

def book_series_edit(request, slug):
    sereis=ss.master.getObjects(slug)
    form = SeriesForm(instance=sereis)
    if 'save' in request.POST:
        print(request.META['HTTP_REFERER'])
        ss.master.commit(
            sereis.series_name,
            series_name  = request.POST['series_name'],
            nyaa_keyword = request.POST['nyaa_keyword'], 
            status       = request.POST.get('status')
        )
        return redirect('book_series', slug)
    elif 'delete' in request.POST:
        ss.master.delete(sereis.series_name)
        return redirect('book_series', slug)
    params={ 'form' : form }
    return render(request, 'master/series_edit.html', params)

# 書籍ダウンロード
def book_download(request, slug):
    try:
        # 書籍取得
        book = sb.retriveBook(slug)
        # ファイルパス取得
        filepath = book.file_path
        # 既読情報更新
        sb.updateReadFlg(book)
        # ダウンロード
        response = StreamingHttpResponse(
            FileWrapper(open(filepath, 'rb'), appconst.chunksize),
            content_type='application/octet-stream'
        )
        response['Content-Length'] = utils.getsize(filepath)
        filename = utils.encode(utils.getFileName(filepath))
        response['Content-Disposition'] = "attachment;  filename='{}'; filename*=UTF-8''{}".format(filename, filename)
        return response
    except Exception as e:
        print(e)
# nyaaダウンロード
def book_nyaa(request, torrent_link):
    model = st.getObjectBookTorrent(torrent_link)
    try:
        # Torrentファイルのダウンロード
        st.downloadTorrentFile(model.torrent_link, model.title)
        # ダウンロード済みの更新
        st.updBookTorrent(torrent_link)
    except Exception as e:
        print(e)
    return redirect('book_series', model.series.slug)
"""
シリーズ一覧・編集
"""
#編集
def book_edit(request, pk):
    book = sb.retriveBook(pk)
    if "save" in request.POST:
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            genrue_id  = request.POST['genrue_name']
            story_by   = request.POST['story_by']
            art_by     = request.POST['art_by']
            title      = request.POST['title']
            sub_title  = request.POST['sub_title']
            volume     = request.POST['volume']

            # コミット
            sb.update(book.file_path, book, genrue_id, story_by, art_by, title, sub_title, volume)
        else:
            messages.error(request, form.errors)
            return redirect('book_edit', pk)
    elif "delete" in request.POST:
        sb.delete(pk)
        return redirect('book_series', book.book.series.slug)
    elif "back" in request.POST:
        return redirect('book_series', book.book.series.slug)
    else:
        # 編集画面へ
        # 初期値設定
        initial={
            'genrue_name':book.genrue_id,
            'story_by'   :book.book.story_by.author_name,
            'art_by'     :book.book.art_by.author_name,
            'title'      :book.book.title,
            'sub_title'  :book.book.sub_title,
            }
        form = BookForm(instance=book, initial=initial)
        bi = si.searchBookInfo(book.genrue_id, book.book.title, book.book.sub_title)
        pdf = utils.replace(book.file_path, appconst.FOLDER_TODOAPPS, appconst.MEDIA_URL)
        return render(request, 'book/book_edit.html', {'form' : form, 'workbook':book, 'bookinfo' : bi , 'images' : '', 'pdf': pdf})
    
    return redirect('book_series', book.book.series.slug)

"""
書籍要修正リスト
"""
def book_revice(request):
    models = sb.reviceList()
    params = {'models' : models}
    return render(request, 'library/book_revice.html', params)

"""
共通（ページネーション）
"""
def pagenation(request, model, *args):
    alias = args[0] if args else 'page'
    paginator = Paginator(model, 20) # 1ページ表示件数設定
    page = request.GET.get(alias) # URLのパラメータから現在のページ番号を取得
    if page:
        request.session[alias] = page
    elif alias in request.session:
        page = request.session[alias] 
    else:
        page = request.GET.get(alias, 1)
    models = paginator.get_page(page) # 指定のページのArticleを取得
    return models