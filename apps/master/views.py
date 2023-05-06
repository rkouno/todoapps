from django.shortcuts import render
from django.shortcuts import redirect

# from
from apps.master.forms import AdultForm

# service
# from apps.master.anime import service as asv
from apps.commons.services.service_anime import master as sa
from apps.commons.services import service_series as ss

# Create your views here.
"""
Video
"""
def adult_list(request):
    adults = sa.retriveAdultVideo()
    params = {'adults' : adults}
    return render(request, 'master/adult_list.html', params)

def adult_edit(request, id):
    adult = sa.getAdultObject(id)
    form = AdultForm(instance=adult)

    if 'save' in request.POST:
        sa.commit(
            id,
            request.POST['title'],
            request.POST['group']
        )
        return redirect('adult_list')
    params={ 'form' : form }
    return render(request, 'master/adult_edit.html', params)

"""
Book
"""
def series_list(request):
    generals = ss.retriveSeries(True)
    adults = ss.retriveSeries(False)
    params={ 
        'generals' : generals,
        'adults' : adults
        }
    return render(request, 'master/series_list.html', params)