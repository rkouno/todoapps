from django.shortcuts import render
from django.shortcuts import redirect
# common
from apps.commons.const import appconst
# from
from apps.master.forms import AdultForm
from apps.master.forms import CategoryForm
from apps.master.forms import AuthorForm
from apps.master.forms import InfoForm
from apps.master.forms import SeriesForm
# service
from apps.commons.services.service_anime import master as sa
from apps.commons.services.service_category import master as ca
from apps.commons.services import service_author as sau
from apps.commons.services import service_series as ss
from apps.commons.services import service_bookInfo as si
from apps.commons.services import service_video as sv

# Create your views here.
"""
Adult Video
"""
# 一覧
def adult_list(request):
    adults = sa.getAll()
    params = {'adults' : adults}
    return render(request, 'master/adult_list.html', params)
# 編集
def adult_edit(request, id):
    adult = sa.get(id)
    form = AdultForm(instance=adult)
    if 'save' in request.POST:
        sa.commit(
            id,
            request.POST['title'],
            request.POST['group'],
            request.POST['score'],
            request.POST['category'],
        )
        try:
            request.session['sort_code'] = appconst.SORT_RECENT
            videos = sv.retriveVideo(appconst.HENTAI, 3)
        except Exception as e:
            print(e)
        return render(request, 'video/video_index.html', { 'videos' : videos, 'sort_code' : appconst.SORT_RECENT})
    params={ 'form' : form }
    return render(request, 'master/adult_edit.html', params)
"""
Category
"""
# 一覧
def category_list(request):
    category = ca.getAll()
    params = {'categories' : category}
    return render(request, 'master/category_list.html', params)

def category_new(request):
    form = CategoryForm(request.POST)
    try:
        if request.method == "POST":
            if form.is_valid():
                ca.commit(
                    slug = None,
                    category  = request.POST['category'], 
                    kana      = request.POST.get('kana'),
                    adult_flg = request.POST['adult_flg'],
                )
                form = CategoryForm()
                return redirect('category_list')
        else:
            form = CategoryForm()

    except Exception as e:
        print(e)
    return render(request, 'master/category_edit.html', {'form': form})
# 編集
def category_edit(request, slug):
    category = ca.get(slug)
    form = CategoryForm(instance=category)
    if 'save' in request.POST:
        ca.commit(
            slug,
            request.POST['category'],
            request.POST.get('kana'),
            request.POST['adult_flg'],
        )
        return redirect('category_list')
    elif 'delete' in request.POST:
        ca.delete(id)
        return redirect('category_list')
    
    params={ 'form' : form }
    return render(request, 'master/category_edit.html', params)

"""
Series
"""
# 一覧
def series_list(request):
    if 'search' in request.POST:
        request.session['txtSearch']=request.POST['txtSearch']
    # 検索条件
    search = request.session.get('txtSearch')
    generals = ss.retriveSeries(True, search)
    adults = ss.retriveSeries(False, search)
    params={ 
        'generals' : generals,
        'adults' : adults
        }
    return render(request, 'master/series_list.html', params)
# 編集
def series_edit(request, slug):
    sereis=ss.master.getObjects(slug)
    form = SeriesForm(instance=sereis)
    if 'save' in request.POST:
        print(request.META['HTTP_REFERER'])
        ss.master.commit(
            sereis.series_name,
            series_name  = request.POST['series_name'],
            nyaa_keyword = request.POST['nyaa_keyword'], 
            status       = request.POST.get('status')
        )
        return redirect('series_list')
    elif 'delete' in request.POST:
        ss.master.delete(sereis.series_name)
        return redirect('series_list')
    params={ 'form' : form }
    return render(request, 'master/series_edit.html', params)
"""
Author
"""
# 一覧
def author_list(request):
    if 'search' in request.POST:
        request.session['txtSearch']=request.POST['txtSearch']
    # 検索条件
    search = request.session.get('txtSearch')
    models = sau.master.retriveAuthors(search)
    params={ 
        'models' : models,
    }
    return render(request, 'master/author_list.html', params)
# 編集
def author_edit(request, id):
    author=sau.get(id)
    form = AuthorForm(instance=author)
    if 'save' in request.POST:
        sau.master.update(
            form,
            request.POST['author_name'],
            request.POST.get('kana'),
        )
        return redirect('author_list')
    elif 'delete' in request.POST:
        sau.master.delete(id)
        return redirect('author_list')
    params={ 'form' : form }
    return render(request, 'master/author_edit.html', params)
"""
Info
"""
# 一覧
def info_list(request):
    if 'search' in request.POST:
        request.session['txtSearch']=request.POST['txtSearch']
    # 検索条件
    search = request.session.get('txtSearch')
    comics = si.master.retriveInfos(search, appconst.COMIC)
    novels = si.master.retriveInfos(search, appconst.NOVEL)
    adults = si.master.retriveInfos(search, appconst.ADULT)
    params={ 
        'comics' : comics,
        'novels' : novels,
        'adults' : adults,
    }
    return render(request, 'master/info_list.html', params)
# 編集
def info_edit(request, book_id):
    info=si.get(book_id)
    form = InfoForm(instance=info)
    form.fields['series'].queryset = ss.seriesList(info.series.series_name)
    if 'save' in request.POST:
        si.master.update(
            form,
            request.POST.getlist('genrue'), 
            request.POST.getlist('story_by'),
            request.POST.getlist('art_by'), 
            request.POST['title'],
            request.POST['sub_title'],
            request.POST.getlist('series'), 
            request.POST.getlist('status'), 
            request.POST.getlist('save_path'), 
        )
        return redirect('info_list')
    elif 'delete' in request.POST:
        si.delete(id)
        return redirect('info_list')
    params={ 'form' : form }
    return render(request, 'master/info_edit.html', params)