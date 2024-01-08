# util
from django.db import transaction
from django.db.models import Q
from django.db.models import Prefetch
from django.db.models import Max
from django.db.models import Subquery
from django.db.models import OuterRef
from django.db.models import Count

# models
from apps.book.models import Author
from apps.book.models import Book
from apps.book.models import Info
"""
Common
"""
# 一意取得
def get(pk):
    try:
        author = Author.objects.get(pk=pk)
        return author
    except Exception as e:
        return Author.objects.get(pk=0)

# 登録
@transaction.atomic
def commit(author_name):
    authors, updated = Author.objects.get_or_create(
        author_name = author_name.strip(),
    )
    if updated:
        authors = Author.objects.filter(author_name=author_name).first()
    return authors

# 成年コミック　一覧取得
def retriveAuthors():
    authors = Author.objects.exclude(author_name='').order_by('author_name')
    return authors

def rawObjects(sql, param):
    authors = Author.objects.raw(sql, param)
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
                prefetch_related('story_by_id')
                        # .order_by('-kana_id','author_name')
        
        # 逆参照（単一掘り下げ）
        # info = authors[0].story_by_id.all().prefetch_related('book')[0].book.all()

        # 逆参照（全件）
        # authors2 = Author.objects.prefetch_related(
        #     Prefetch('story_by_id', queryset=Info.objects.all(), to_attr='infos')
        # ).all()\
        # .prefetch_related(
        #     Prefetch('infos__book', queryset=Book.objects.all().annotate(Max('volume')), to_attr='books')
        # ).all()

        # for a in authors2:
        #     for b in a.infos:
        #         for c in b.books:
        #             print(c.volume)

        authors = Author.objects.prefetch_related('story_by_id').exclude(story_by_id__book=None).all().\
        annotate(author_id=Max('id'),
                 story_by=Max('author_name'),
                 series=Max('story_by_id__series'),
                 maxVol=Count('story_by_id__book__volume')
                 ).\
                 values('author_id','story_by', 'maxVol', 'series').\
                    order_by('story_by')
        return authors
    
    def update(form, author_name, kana_id):
        author = form.save(commit=False)
        author.author_name = author_name
        author.kana_id = kana_id
        author.save()
    
    def delete(id):
        Author.objects.get(pk=id).delete()