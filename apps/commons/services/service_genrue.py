# model
from apps.book.models import Genrue

# 全件取得
def getAll():
    genrue = Genrue.objects.all()
    return genrue

# キー検索
def getObject(pk):
    genrue=Genrue.objects.get(pk=pk)
    return genrue
