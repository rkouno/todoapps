import secrets

from django.shortcuts import redirect, render

from apps.commons.const import appconst

from . import service, service_pdf

# Create your views here.
"""
PDF作成
"""
def create_list(request):
    list = service_pdf.getList()
    return render(request, 'book/create_list.html', {'list' : list})

"""
一般コミック
"""
def book_list(request):
    return render(request, 'book/book_list.html', {})

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