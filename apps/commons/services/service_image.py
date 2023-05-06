from django.db import connection

# common
from apps.commons.util import utils
from apps.commons.const import appconst

# db
from apps.book.models import Image

# 画像ファイルリスト作成
def getImages(path):
    Image.objects.all().delete()
    # Autoincremantのリセット
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'book_image'")
    
    for list in sorted(utils.getFiles(f'{path}/', appconst.EXTENTION_IMAGE), key=utils.natural_keys):
        list = list.replace('\\','/')
        url = list.replace(appconst.FOLDER_TORRENT, appconst.TORRENT_URL)
        Image.objects.create(img_link = url, path = list)
# 画像ファイルの取得
def retriveImage():
    return Image.objects.all()
# 画像ファイルの削除
def delImage(id):
    image = Image.objects.get(pk=id)
    utils.fileDelete(image.path)
    Image.objects.get(pk=id).delete()
