from apps.book.models import Status

def get(pk):
    series = Status.objects.get(pk=pk)
    return series

def getAll():
    return Status.objects.all()

# シリーズの取得
def getObject(pk):
    status = Status.objects.filter(slug=pk).first()
    return status