# util
from django.db.models import Q
from django.db import transaction

# models
from apps.book.models import Author

"""
Common
"""
# 一意取得
def get(pk):
    author = Author.objects.get(pk=pk)
    return author

# 登録
@transaction.atomic
def commit(author_name):
    authors, updated = Author.objects.update_or_create(
        author_name = author_name.strip(),
    )
    if updated:
        authors = Author.objects.filter(author_name=author_name).first()
    return authors

# 成年コミック　一覧取得
def retriveAuthors():
    authors = Author.objects.exclude(author_name='').order_by('author_name')
    return authors

def rawObjects(sql):
    authors = Author.objects.raw(sql)
    return authors

def searchAuthor(filter):
    authors = Author.objects.filter(filter).order_by('author_name')
    return authors

"""
Master
"""
class master:
    def retriveAuthors(txt):
        filter=Q(author_name__icontains=txt) if txt else Q()
        authors = Author.objects.exclude(author_name='').\
            filter(filter).\
                order_by('author_name')
        return authors
    
    def update(form, author_name):
        author = form.save(commit=False)
        author.author_name = author_name
        author.save()
    
    def delete(author_id):
        Author.objects.get(pk=author_id).delete()