from ctypes import util
from apps.commons.util import utils
from apps.book.models import book
from apps.book.models import info
from apps.book.models import author
from apps.commons.const import appconst
import img2pdf 
import os

class book_util:
    
    def get_genrue_id(genrue_name):
        if '一般コミック' in genrue_name:
            return 1
        elif '一般小説' in genrue_name:
            return 2
        elif '成年コミック' in genrue_name:
            return 3
        else:
            return 0
        
    def get_genrue_name(geunre_id):
        if geunre_id == 1:
            return '一般コミック'
        elif geunre_id == 2:
            return '一般小説'
        elif geunre_id == 3:
            return '成年コミック'
        elif geunre_id == 4:
            return '成年小説'
        else:
            return ''
    
    def get_title(genrue_id, title):
        print(title)
        sql = f"SELECT * FROM BOOK_INFO WHERE '{title}' LIKE '%' || TITLE || '%' || SUB_TITLE || '%' AND ({genrue_id} = 0 OR GENRUE_ID = {genrue_id}) AND SUB_TITLE <> '' "
        bi = info.objects.raw(sql)
        if bi:
            str_len = len(title)
            for inf in bi:
                if str_len > len(title.replace(inf.title,'')):
                    str_len = len(title.replace(inf.title,'').replace(inf.sub_title,''))
                    res_genrue_id = inf.genrue_id
                    res_title = inf.title
                    res_sub_title = inf.sub_title

            return (res_genrue_id, res_title, res_sub_title, 'Edit')
        sql = f"SELECT * FROM BOOK_INFO WHERE '{ title }' LIKE '%' || TITLE || '%' || SUB_TITLE || '%' AND ({genrue_id} = 0 OR GENRUE_ID = {genrue_id}) "
        bi = info.objects.raw(sql)
        if bi:
            str_len = len(title)
            for inf in bi:
                if str_len > len(title.replace(inf.title,'').replace(inf.sub_title,'')):
                    str_len = len(title.replace(inf.title,'').replace(inf.sub_title,''))
                    res_genrue_id = inf.genrue_id
                    res_title = inf.title

            return (res_genrue_id, res_title, '', 'Edit')
        genrue = utils.getRegex(title, appconst.REGEX_GENRUE)
        author = utils.getRegex(title, appconst.REGEX_AUTHOR)
        volume = utils.getRegex(title, appconst.REGEX_VOLUME)

        title = title.replace(genrue, '').replace(author, '').replace(volume, '').replace('.pdf', '').replace('.epub', '')
        return genrue_id, title , '', 'None'

    def get_author(str):
        sql = f"SELECT * FROM BOOK_AUTHOR WHERE '{ str }' LIKE '%' || AUTHOR_NAME || '%' AND AUTHOR_NAME <> '' "
        authors = author.objects.raw(sql)
        if authors:
            return authors[0].author_name
        else:
            return utils.getRegex(str, appconst.REGEX_AUTHOR_NONE_BRACKETS)

    def get_book_name(genrue_name, story_by, art_by, title, sub_title, volume):
        
        author = story_by 
        if len(art_by.strip()) > 0:
            author += f'×{art_by}'
        if sub_title:
            title = f'{title} {sub_title}'
        if volume == 0:
            episode = ''
        elif volume == '0':
            episode = ''
        else:
            episode = f'第{volume}巻'
        
        if title:
            book_name = f'({genrue_name})【{author}】{title} {episode}'.strip()
        else:
            book_name = ''

        return book_name

    def get_save_path(genrue_id):
        if genrue_id == 1:
            save_path = appconst.FOLDER_BOOK_COMIC
        elif genrue_id == 2:
            save_path = appconst.FOLDER_BOOK_NOVEL
        elif genrue_id == 3:
            save_path = appconst.FOLDER_BOOK_ADULT
        elif genrue_id == 4:
            save_path = appconst.FOLDER_BOOK_ADULT_NOVEL
        else:
            save_path = ''
        return save_path
    
    def get_book_id(genrue_id, story_by, art_by, title, sub_title):
        bi = info.objects.filter(genrue_id = genrue_id, story_by = story_by, art_by = art_by, title = title, sub_title = sub_title).first()
        if not bi:
            return 0
        return bi.book_id

    def create_pdf(img_path, pdf_path):
        img_list = []
        for file in os.listdir(img_path):
            extention = os.path.splitext(file)[1]
            if ".jpg" == extention:
                img_list.append(f'{img_path}/{file}')
            elif ".png" == extention:
                img_list.append(f'{img_path}/{file}')
            elif ".jpeg" == extention:
                img_list.append(f'{img_path}/{file}')
        
        img_list = sorted(img_list)

        with open(f'{pdf_path}', "wb") as f: 
            f.write(img2pdf.convert(img_list))
        f.close()