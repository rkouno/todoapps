# util
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages

# common
from django.core.paginator import Paginator
from apps.commons.util import security
from apps.commons.util import utils
from apps.commons.const import appconst

# service
from apps.commons.services import service_bookInfo as sbi
from apps.commons.services import service_workbook as sw
from apps.commons.services import service_image    as si
from apps.commons.services import service_torrent  as st
from apps.commons.services import service_book     as sb
from apps.commons.services.service_torrent import download

# from
from apps.book.froms import WorkBookForm

"""
DOWNLOAD
"""
# Nyaa>一覧
def nyaa_list(request):
    try:
        torrents = st.retriveTorrentNyaa()
        params   = { 'torrents' : torrents }
        return render(request, 'download/nyaa_list.html', params)
    except Exception as e:
        print(e)
        messages.error(request. e)

# Nyaa>一覧の更新
def nyaa_webscrap(request):
    try:
        download.nyaa_webscrapping()
    except Exception as e:
        print(e)
        messages.error(request. e)
    return redirect('nyaa_list')

# Nyaa>ダウンロード
def nyaa_download(request, pk):
    try:
        model = st.getObjectBookTorrent(pk)
        # Torrentファイルのダウンロード
        st.downloadTorrentFile(model.torrent_link, model.title)
        # ダウンロード済みの更新
        st.updBookTorrent(pk)
    except Exception as e:
        print(e)
        messages.error(request, e)
    return redirect('nyaa_list')

# Sukebei>一覧
def sukebei_list(request):
    try:
        torrents = st.retriveTorrentAdult()
        params   = { 'torrents' : torrents }
        return render(request, 'download/sukebei_list.html', params)
    except Exception as e:
        print(e)
        messages.error(request, e)

# Sukebei>一覧の更新
def sukebei_webscrap(request):
    try:
        download.sukebei_webscrapping()
    except Exception as e:
        print(e)
        messages.error(request, e)
    return redirect('sukebei_list')

# Sukebei>ダウンロード
def sukebei_download(request, pk):
    try:
        model = st.getObjectBookTorrent(pk)
        # Torrentファイルのダウンロード
        st.downloadTorrentFile(model.torrent_link, model.title)
        # ダウンロード済みの更新
        st.updBookTorrent(pk)
    except Exception as e:
        print(e)
        messages.error(request, e)

    return redirect('sukebei_list')

# Check>一覧
def check_list(request):
    try:
        params ={
            "comics" : download.SeriesDownlaod(1),
            "novels" : download.SeriesDownlaod(2),
            "adults" : download.SeriesDownlaod(3),
        }
    except Exception as e:
        print(e)
        messages.error(request, e)
    return render(request, 'download/check_list.html', params)

# Check>Comic/Novel/Adult
def book_webscrap(request):
    try:
        # 一般コミック
        download.newSearchTorrent(1)
        # 一般小説
        download.newSearchTorrent(2)
        # 成年コミック
        download.newSearchTorrent(3)
    except Exception as e:
        print(e)
        messages.error(request, e)
    return redirect('check_list')

# Check>Modal(Ajax)
def book_list(request):
    try:
        series_name = request.POST['series_name']
        genrue_id = request.POST['genrue_id']
        bi = sb.retriveSeries(series_name, genrue_id)
        return JsonResponse(list(bi.values()), safe=False)
    except Exception as e:
        print(e)
        messages.error(request, e)
    return JsonResponse('', safe=False)

def check_nyaa_download(request, pk):
    try:
        model = st.getObjectBookTorrent(pk)
        # Torrentファイルのダウンロード
        st.downloadTorrentFile(model.torrent_link, model.title)
        # ダウンロード済みの更新
        st.updBookTorrent(pk)
    except Exception as e:
        print(e)
        messages.error(request, e)
    return redirect('check_list')

def check_sukebei_download(request, pk):
    try:
        model = st.getObjectBookTorrent(pk)
        # Torrentファイルのダウンロード
        st.downloadTorrentFile(model.torrent_link, model.title)
        # ダウンロード済みの更新
        st.updBookTorrent(pk)
    except Exception as e:
        print(e)
        messages.error(request, e)
    return redirect('check_list')

def check_edit(request, pk):
    book = sb.retriveBook(pk)
    pdf = utils.replace(book.file_path, appconst.FOLDER_TODOAPPS, appconst.MEDIA_URL)
    return redirect(pdf)
"""
BOOK
"""
# ------------
# 一覧画面
# ------------
def workbook_create(request):
    try:
        if 'getList' in request.POST:
            #bat実行
            # sw.unzip()
            sw.unzip()
            # 最新一覧取得
            sw.getLatestList()
            request.session.clear()
        elif 'clear' in request.POST:
            sw.clear()
        elif 'setting' in request.POST:
            sw.settting()
        elif 'replace' in request.POST:
            sw.replace(request.POST['txtReplace_b'], request.POST['txtReplace_a'], request.POST.get('isRegex'))
        elif 'search' in request.POST:
            request.session['txtSearch']   = request.POST.get('txtSearch')
            request.session['isRegex']     = getKey(request, 'isRegex')
            request.session['nonecheck']   = getKey(request, 'nonecheck')
            request.session['newcheck']    = getKey(request, 'newcheck')
            request.session['delcheck']    = getKey(request, 'delcheck')
            request.session['createcheck'] = getKey(request, 'createcheck')
        elif 'execute' in request.POST:
            sw.execute()
            sw.settting()
    except Exception as e:
        print(e)
        messages.error(request, e)

    # 一覧取得
    model = sw.retriveWorkbooks(getSession(request, 'txtSearch'),
                                getSession(request, 'nonecheck'),
                                getSession(request, 'newcheck'),
                                getSession(request, 'delcheck'),
                                getSession(request, 'createcheck'))
    # ページネーション
    model = pagenation(request, model)
    return render(request, 'book/book_create.html', {'workbooks' : model})

# 処理変更
def workbook_process(request):
    id      = request.POST['id']
    process = request.POST['process']
    sw.process(id, process)
    return JsonResponse('', safe=False)

# ------------
# 編集画面
# ------------
# 編集画面
def workbook_edit(request, pk):
    model = sw.getWorkbook(pk)
    if "save" in request.POST:
        if security.exist_submit_token(request):
            try:
                form = WorkBookForm(data=request.POST, instance=model)
                print(form.errors)
                if form.is_valid():
                    sw.update(form, 
                            genrue_id := request.POST['genrue_name'], 
                            story_by  := request.POST['story_by'],
                            art_by    := request.POST['art_by'], 
                            title     := request.POST['title'], 
                            sub_title := request.POST['sub_title'], 
                            volume    := request.POST['volume'],
                            )
                    request.session['submit_token'] = security.set_submit_token(request)
                    return redirect('workbook_create')
            except Exception as e:
                print(e)
                messages.error(request, e)
                return redirect("workbook_edit", pk)
    elif "next" in request.POST:
        try:
            model = sw.getWorkbook(pk)
            form = WorkBookForm(request.POST, instance=model)
            if form.is_valid():
                sw.update(form, 
                            genrue_id := request.POST['genrue_name'], 
                            story_by  := request.POST['story_by'],
                            art_by    := request.POST['art_by'], 
                            title     := request.POST['title'], 
                            sub_title := request.POST['sub_title'], 
                            volume    := request.POST['volume'],
                            )
            next=sw.next(pk)
            request.session['submit_token'] = security.set_submit_token(request)
            return redirect("workbook_edit", next)
        except Exception as e:
            print(e)
            messages.error(request, e)
    else:
        try:
            si.getImages(model.path)
            info    = sbi.searchBookInfo(model.genrue_id, model.title, model.sub_title)
            images  = si.retriveImage()
            pdf     = sw.getPDFpath(model.name)
            init    = dict(genrue_name=model.genrue_id)
            form    = WorkBookForm(instance=model, initial=init)
            params  = {'form' : form, 'workbook':model, 'bookinfo' : info , 'images' : images, 'pdf': pdf}
            request.session['submit_token'] = security.set_submit_token(request)
            return render(request, 'book/book_edit.html', params)
        except Exception as e:
            print(e)
            messages.error(request, e)
    request.session['submit_token'] = security.set_submit_token(request)
    return redirect('workbook_create')
# 削除
def workbook_delete(request, pk):
    sw.process(pk, 'Delete')
    return redirect('workbook_create')
# 書籍選択リスト
def book_info(request):
    genrue_id = request.POST['genrueID']
    title     = request.POST['title']
    sub_title = request.POST['subTitle']
    bi        = sbi.searchBookInfo(genrue_id, title, sub_title)
    return JsonResponse(list(bi), safe=False)
# 画像削除
def book_delimage(request):
    image_id     = request.POST['image_id']
    si.delImage(image_id)
    images  = si.retriveImage()
    return JsonResponse(list(images.values()), safe=False)

"""
共通（ページネーション）
"""
def pagenation(request, model):
    paginator = Paginator(model, 15) # 1ページ表示件数設定
    page = request.GET.get('page') # URLのパラメータから現在のページ番号を取得
    if page:
        request.session['page'] = page
    elif 'page' in request.session:
        page = request.session['page'] 
    else:
        page = request.GET.get('page', 1)
    models = paginator.get_page(page) # 指定のページのArticleを取得
    return models

def getSession(request, key):
    try:
        return request.session[key]
    except Exception as e:
        return ''

def getKey(request, key):
    try:
        print(request.POST.get(key))
        return 'checked' if request.POST.get(key) else ''
    except Exception as e:
        return request.session[key]