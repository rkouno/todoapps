import secrets
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
import os
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from apps.book.froms import WorkBookForm, BookForm
from apps.book.models import Workbook, book
from apps.commons.const import appconst
from apps.commons.util import utils
from . import service, service_pdf, service_book
from django.forms.models import model_to_dict

"""
PDF作成
"""
# 一覧画面
def create_list(request):
    if request.method in "POST":
        if "list" in request.POST:
            # 一覧取得
            service_pdf.getList()
        elif "setting" in request.POST:
            # 名称設定
            service_pdf.setName()
        elif "execute" in request.POST:
            # 実行
            service_pdf.create()
        elif "replace" in request.POST:
            # 置換
            txtSearch = request.POST['txtSearch']
            txtReplace_b = request.POST['txtReplace_b']
            txtReplace_a = request.POST['txtReplace_a']
            service_pdf.replace(txtSearch, txtReplace_b, txtReplace_a)
        elif "search" in request.POST:
            search = request.POST.get('txtSearch')
            Workbooks = service_pdf.searchWorkbooks(search)
            return render(request, 'book/create_list.html', {'Workbooks' : Workbooks})
    
    Workbooks = service_pdf.retriveWorkbooks()
    return render(request, 'book/create_list.html', {'Workbooks' : Workbooks})
    
# 編集画面
def book_edit(request ,pk):
    workbook = get_object_or_404(Workbook, pk=pk)

    if "save" in request.POST or "next" in request.POST:
        form = WorkBookForm(request.POST, instance=workbook)
        if form.is_valid():
            service_pdf.commit(
                form,
                genrue_id = request.POST['genrue_name'], 
                story_by = request.POST['story_by'],
                art_by = request.POST['art_by'],
                title = request.POST['title'],
                sub_title = request.POST['sub_title'],
                volume = request.POST['volume'],
            )
            if "next" in request.POST:
                next=service_pdf.next(pk)
                return redirect("book_edit", pk=next)
        else:
            # データが不正だったらフォームを再描画する
            return render(request, 'book/book_edit.html', {'form' : form, 'workbook':workbook})
    elif "delete" in request.POST:
        service_pdf.delete(workbook.id, workbook.path)
    else:
        form = WorkBookForm(instance=workbook,initial = {'selected': 2})
        bi = service_book.retriveBookInfo(workbook.genrue_id, workbook.title, workbook.sub_title)
        images = service_book.retriveImage(workbook.path)
        pdf = appconst.TORRENT_URL + workbook.name
        return render(request, 'book/book_edit.html', {'form' : form, 'workbook':workbook, 'bookinfo' : bi , 'images' : images, 'pdf': pdf})

    return redirect('create_list')

def book_info(request):
    genrue_id =  request.POST['genrueID']
    title =  request.POST['title']
    sub_title =  request.POST['subTitle']
    bi = service_book.retriveBookInfo(genrue_id, title, sub_title)
    bi =[model_to_dict(l) for l in bi]
    return JsonResponse(bi,safe=False)

# 処理変更
def book_process(request):
    id = request.POST['id']
    process = request.POST['process']
    service_pdf.process(id, process)
    
    return JsonResponse('',safe=False)
"""
一般コミック
"""
def book_comic(request):
    info = service_book.retriveInfo(appconst.COMIC)
    return render(request, 'book/book_list.html', {'books':'', 'info':info})
"""
一般小説
"""
def book_novel(request):
    info = service_book.retriveInfo(appconst.NOVEL)
    return render(request, 'book/book_list.html', {'books':'', 'info':info})
"""
アダルト
"""
def book_adult(request):
    authors = service_book.retriveAuthors()
    return render(request, 'book/book_adult.html', {'books':'', 'authors':authors})
"""
要修正リスト
"""
def book_revice(request):
    books = service_book.retriveFix()
    return render(request, 'book/book_revice.html', {'books':books})

# 編集画面
def book_fix(request ,pk):
    b = get_object_or_404(book, pk=pk)

    if "save" in request.POST:
        form = BookForm(request.POST, instance=b)
        if form.is_valid():
            service_book.commit(form)
    elif "delete" in request.POST:
        service_book.delete(b.id, b.file_path)
    else:
        form = BookForm(instance=b,initial = {'selected': 2})
        bi = service_book.retriveBookInfo(b.genrue_id, b.title, b.sub_title)
        pdf = b.file_path.replace(appconst.FOLDER_TODOAPPS, appconst.MEDIA_URL)
        return render(request, 'book/book_edit.html', {'form' : form, 'workbook':b, 'bookinfo' : bi , 'images' : '', 'pdf': pdf})

    return redirect('book_revice')

"""
書籍
"""
def book_detail(request,alias ,pk):
    if alias in "adult":
        books = service_book.retriveAdultBooks(pk)
    else:
        books = service_book.retriveBooks(pk)
    return render(request, 'book/book_list.html', {'books':books, 'info':''})

"""
ダウンロード
"""
def book_download(request, pk):
    filepath ,book_name = service_book.download(pk)
    response = StreamingHttpResponse(
        FileWrapper(open(filepath, 'rb'), appconst.chunksize),
        content_type='application/octet-stream'
    )
    response['Content-Length'] = os.path.getsize(filepath)
    filename = utils.encode(os.path.basename(filepath))
    response['Content-Disposition'] = "attachment;  filename='{}'; filename*=UTF-8''{}".format(filename, filename)
    return response

"""
成年コミック
"""
# 一覧
def adult_list(request):
    try:
        torrents = service.retriveTorrent()
        return render(request, 'book/adult_list.html', {'torrents': torrents})
    except Exception as e:
        print(e)
    return render(request, 'book/adult_list.html', {})

# Web scraping
def adult_webscraping(request):
    service.webscraping()
    return redirect('adult_list')

# ダウンロード
def adult_download(request, pk):
    service.download(pk)
    return redirect('adult_list')