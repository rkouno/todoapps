# model
from apps.book.models import Genrue


def getObject(pk):
    genrue=Genrue.objects.get(pk=pk)
    return genrue