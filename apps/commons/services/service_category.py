#utils
from django.shortcuts import get_object_or_404

#django db
from apps.anime.models import Category
from apps.anime.models import Kana

class master:
    def getAll():
        category = Category.objects.all().order_by('category')
        return category

    def get(slug):
        return get_object_or_404(Category, pk=slug)

    def commit(slug, category, kana, adult_flg):
        Category.objects.update_or_create(
            slug = slug,
            defaults = {
                'category'  : category,
                'adult_flg' : True if adult_flg=='on' else False,
                'kana'      : Kana.objects.get(id=kana)
            }
        )
        
    def delete(slug):
        category = master.get(slug)
        category.delete()

            