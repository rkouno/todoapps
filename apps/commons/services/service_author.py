# util
from django.db import transaction

# models
from apps.book.models import Author

# 成年コミック　一覧取得
def retriveAuthors():
    sql =	"SELECT "\
        + "      A.AUTHOR_ID "\
        + "    , A.AUTHOR_NAME "\
        + "    , MIN(BB.READ_FLG) AS READ_FLG "\
        + "FROM "\
        + "    BOOK_AUTHOR A "\
        + "    INNER JOIN BOOK_BOOK BB "\
        + "        ON A.AUTHOR_ID = BB.STORY_BY_ID "\
        + "WHERE "\
        + "    A.GENRUE_ID IN (3, 4) "\
        + "GROUP BY "\
        + "    A.AUTHOR_ID "\
        + "    , A.AUTHOR_NAME "\
        + "ORDER BY "\
        + "    BB.READ_FLG ASC "\
        + "    , BB.REGIST_DATE DESC "

    authors = Author.objects.raw(sql)
    return authors

@transaction.atomic
def author_commit(genrue_id, author_name):
    authors, created = Author.objects.get_or_create(
        author_name  = author_name.strip(),
        genrue_id    = genrue_id
    )
    if created:
        authors = Author.objects.filter(genrue_id=genrue_id, author_name=author_name).first()
    return authors

