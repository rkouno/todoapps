# util
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse

# common
from django.core.paginator import Paginator

# service
from apps.commons.services import service_bookInfo as sbi
from apps.commons.services import service_workbook as sw
from apps.commons.services import service_image    as si
from apps.commons.services import service_torrent  as st

# from
from apps.book.froms import WorkBookForm

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
"""
DOWNLOAD
"""
# Sukebei 一覧
def download_sukebei(request):
    torrents = st.retriveTorrent()
    params   = { 'torrents' : torrents }
    return render(request, 'download/download_sukebei.html', params)
# 一覧の更新
def download_webscrap(request):
    st.webscrapping()
    return redirect('download_sukebei')
# ダウンロード
def download_sukebei_comic(request, pk):
    model = st.getObjectBookTorrent(pk)
    # Torrentファイルのダウンロード
    st.downloadTorrentFile(model.torrent_link, model.title)
    # ダウンロード済みの更新
    st.updBookTorrent(pk)
    return redirect('download_sukebei')
"""
BOOK
"""
# ------------
# 一覧画面
# ------------
def workbook_create(request):
    if 'getList' in request.POST:
        # 最新一覧取得
        sw.getLatestList()
        request.session.clear()
    elif 'setting' in request.POST:
        sw.settting()
    elif 'replace' in request.POST:
        sw.replace(request.POST['txtReplace_b'], request.POST['txtReplace_a'], request.POST.get('isRegex'))
    elif 'search' in request.POST:
        request.session['txtSearch']=request.POST['txtSearch']
    elif 'execute' in request.POST:
        sw.execute()
    # 検索条件
    search = request.session.get('txtSearch')
    # 一覧取得
    model = sw.retriveWorkbooks(search)
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
        form = WorkBookForm(data=request.POST, instance=model)
        print(form.errors)
        if form.is_valid():
            sw.commit(form, 
                      genrue_id := request.POST['genrue_name'], 
                      story_by  := request.POST['story_by'],
                      art_by    := request.POST['art_by'], 
                      title     := request.POST['title'], 
                      sub_title := request.POST['sub_title'], 
                      volume    := request.POST['volume'],
                      )
            return redirect('workbook_create')
    elif "next" in request.POST:
        try:
            model = sw.getWorkbook(pk)
            form = WorkBookForm(request.POST, instance=model)
            if form.is_valid():
                sw.commit(form, 
                            genrue_id := request.POST['genrue_name'], 
                            story_by  := request.POST['story_by'],
                            art_by    := request.POST['art_by'], 
                            title     := request.POST['title'], 
                            sub_title := request.POST['sub_title'], 
                            volume    := request.POST['volume'],
                            )
            next=sw.next(pk)
            return redirect("workbook_edit", next)
        except Exception as e:
            print(e)
    else:
        si.getImages(model.path)
        info    = sbi.searchBookInfo(model.genrue_id, model.title, model.sub_title)
        images  = si.retriveImage()
        pdf     = sw.getPDFpath(model.name)
        init    = dict(genrue_name=model.genrue_id)
        form    = WorkBookForm(instance=model, initial=init)
        params  = {'form' : form, 'workbook':model, 'bookinfo' : info , 'images' : images, 'pdf': pdf}
        return render(request, 'book/book_edit.html', params)
    
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
Master
"""










    # if request.method in "POST":
    #     if "list" in request.POST:
    #         # 一覧取得
    #         service_pdf.getList()
    #     elif "setting" in request.POST:
    #         # 名称設定
    #         service_pdf.setName()
    #     elif "execute" in request.POST:
    #         # 実行
    #         service_pdf.create()
    #     elif "replace" in request.POST:
    #         # 置換
    #         txtSearch = request.POST['txtSearch']
    #         txtReplace_b = request.POST['txtReplace_b']
    #         txtReplace_a = request.POST['txtReplace_a']
    #         isRegex = request.POST.get('isRegex')
    #         service_pdf.replace(txtSearch, txtReplace_b, txtReplace_a, isRegex)
    #     elif "search" in request.POST:
    #         search = request.POST.get('txtSearch')
    #         Workbooks = service_pdf.searchWorkbooks(search)
    #         paginator = Paginator(Workbooks, 20) # 1ページに10件表示
    #         p = request.GET.get('page', 1) # URLのパラメータから現在のページ番号を取得
    #         Workbooks = paginator.get_page(p) # 指定のページのArticleを取得
    #         return render(request, 'book/create_list.html', {'Workbooks' : Workbooks})

    # Workbooks = service_pdf.retriveWorkbooks()
    # paginator = Paginator(Workbooks, 20) # 1ページに10件表示
    # page = request.GET.get('page') # URLのパラメータから現在のページ番号を取得

    # if page:
    #     request.session['page'] = page
    # elif 'page' in request.session:
    #     page = request.session['page'] 
    # else:
    #     page = request.GET.get('page', 1)

    # Workbooks = paginator.get_page(page) # 指定のページのArticleを取得
    # return render(request, 'book/create_list.html', {'Workbooks' : Workbooks})
    
# 編集画面
# def book_edit(request ,pk):
#     workbook = get_object_or_404(Workbook, pk=pk)

#     if "save" in request.POST or "next" in request.POST:
#         form = WorkBookForm(request.POST, instance=workbook)
#         if form.is_valid():
#             service_pdf.commit(
#                 form,
#                 genrue_id = request.POST['genrue_name'], 
#                 story_by = request.POST['story_by'],
#                 art_by = request.POST['art_by'],
#                 title = request.POST['title'],
#                 sub_title = request.POST['sub_title'],
#                 volume = request.POST['volume'],
#             )
#             if "next" in request.POST:
#                 try:
#                     next=service_pdf.next(pk)
#                     return redirect("book_edit", pk=next)
#                 except Exception as e:
#                     print(e)
#         else:
#             # データが不正だったらフォームを再描画する
#             return render(request, 'book/book_edit.html', {'form' : form, 'workbook':workbook})
#     elif "delete" in request.POST:
#         service_pdf.delete(workbook.id, workbook.path)
#     else:
#         form = WorkBookForm(instance=workbook,initial = {'selected': 2})
#         bi = service_book.retriveBookInfo(workbook.genrue_id, workbook.title, workbook.sub_title)
#         images = service_book.retriveImage(workbook.path)
#         if not images:
#             pdf = appconst.TORRENT_URL + workbook.name
#         else:
#             pdf = None
#         return render(request, 'book/book_edit.html', {'form' : form, 'workbook':workbook, 'bookinfo' : bi , 'images' : images, 'pdf': pdf})

#     return redirect('create_list')

# def book_info(request):
#     genrue_id =  request.POST['genrueID']
#     title =  request.POST['title']
#     sub_title =  request.POST['subTitle']
#     bi = service_book.retriveBookInfo(genrue_id, title, sub_title)
#     bi =[model_to_dict(l) for l in bi]
#     return JsonResponse(bi,safe=False)


# """
# 一般コミック
# """
# def book_comic(request):
#     info = service_book.retriveInfo(appconst.COMIC)
#     return render(request, 'book/book_list.html', {'books':'', 'info':info})
# """
# 一般小説
# """
# def book_novel(request):
#     info = service_book.retriveInfo(appconst.NOVEL)
#     return render(request, 'book/book_list.html', {'books':'', 'info':info})
# """
# アダルト
# """
# def book_adult(request):
#     authors = service_book.retriveAuthors()
#     return render(request, 'book/book_adult.html', {'books':'', 'authors':authors})
# """
# 要修正リスト
# """
# def book_revice(request):
#     books = service_book.retriveFix()
#     return render(request, 'book/book_revice.html', {'books':books})

# def book_check(request):
#     books = service_book.check2()
#     return render(request, 'book/book_revice.html', {'noneBooks':books})

# # 編集画面
# def book_fix(request ,pk):
#     b = Book.objects.filter(slug=pk).first()

#     if "save" in request.POST:
#         form = BookForm(request.POST, instance=b)
#         if form.is_valid():
#             service_book.commit(form,pk)
#             return redirect('book_fix')
#     elif "delete" in request.POST:
#         service_book.delete(b.file_path)
#         if b.genrue_id == 1:
#             return redirect('book_comic', b.book_id)
#         elif b.genrue_id == 1:
#             return redirect('book_novel', b.book_id)
#         elif b.genrue_id == 1:
#             return redirect('book_adult', b.book_id)
#     else:
#         form = BookForm(instance=b,initial = {'selected': 2})
#         bi = service_book.retriveBookInfo(b.genrue_id, b.title, b.sub_title)
#         pdf = b.file_path.replace(appconst.FOLDER_TODOAPPS, appconst.MEDIA_URL)
#         return render(request, 'book/book_edit.html', {'form' : form, 'workbook':b, 'bookinfo' : bi , 'images' : '', 'pdf': pdf})

#     return redirect('book_revice')

# def book_none(request ,file):
#     form = BookForm(initial = {'selected': 2})
#     pdf = file.replace(appconst.FOLDER_TODOAPPS, appconst.MEDIA_URL)
#     return render(request, 'book/book_edit.html', {'form' : form, 'pdf': pdf})

# """
# 書籍
# """
# def book_detail(request,alias ,pk):
#     if alias in "adult":
#         books = service_book.retriveAdultBooks(pk)
#     else:
#         books = service_book.retriveBooks(pk)
#     return render(request, 'book/book_list.html', {'books':books, 'info':''})

# """
# ダウンロード
# """
# import logging
# def book_download(request, slug):
#     logfile = appconst.FOLDER_BASE+"test.log"
#     logging.basicConfig(filename=logfile,level=logging.DEBUG)
#     try:
#         filepath = service_book.download(slug)
#         response = StreamingHttpResponse(
#             FileWrapper(open(filepath, 'rb'), appconst.chunksize),
#             content_type='application/octet-stream'
#         )
#         response['Content-Length'] = os.path.getsize(filepath)
#         filename = utils.encode(os.path.basename(filepath))
#         response['Content-Disposition'] = "attachment;  filename='{}'; filename*=UTF-8''{}".format(filename, filename)
#         return response
#     except Exception as e:
#         print(e)
#         logging.info(e)
#     redirect('adult_list')
# """
# 成年コミック
# """
# # 一覧
# def adult_list(request):
#     try:
#         torrents = service.retriveTorrent()
#         return render(request, 'book/adult_list.html', {'torrents': torrents})
#     except Exception as e:
#         print(e)
#     return render(request, 'book/adult_list.html', {})

# # Web scraping
# def adult_webscraping(request):
#     service.webscrapping()
#     return redirect('adult_list')

# # ダウンロード
# def adult_download(request, pk):
#     service.download(pk)
#     return redirect('adult_list')

# def nyaa_download(request):
#     try:
#         books = service.retriveNyasBooks()
#         return render(request, 'book/nyaa_download.html', {'books': books})
#     except Exception as e:
#         print(e)
#     return render(request, 'book/nyaa_download.html', {})

# def sukebe_download(request):
#     try:
#         books = service.retriveSukebeBooks()
#         return render(request, 'book/nyaa_download.html', {'adults': books})
#     except Exception as e:
#         print(e)
#     return render(request, 'book/nyaa_download.html', {})

# def download(request, alias, pk):
#     if alias in "book":
#         word = service.bookTitle(pk)
#         service.nyaascraping(word, appconst.BOOK_URL, pk)
#         torrents = service.retriveDownloadBooks(pk)
#         books = service.retriveBooks(pk)
#         service.updateInfo(pk)
#         return render(request, 'book/nyaa_list.html', {'torrents': torrents, 'books':books})
#     else:
#         word = service.authorName(pk)
#         service.nyaascraping(word, appconst.SUKEBEI_URL)
#         books = service.retriveSukebeBooks()
#         return render(request, 'book/nyaa_download.html', {'adults': books})

# def nyaa(request, id, book_id):
#     service.download(id)
#     torrents = service.retriveDownloadBooks(book_id)
#     books = service.retriveBooks(book_id)
        
#     return render(request, 'book/nyaa_list.html', {'torrents': torrents, 'books':books})
 