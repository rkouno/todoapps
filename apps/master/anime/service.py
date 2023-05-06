from apps.anime.models import Adult
from django.shortcuts import get_object_or_404

def retriveAdultVideo():
    adults = Adult.objects.all()
    return adults

def getAdultObject(id):
    return get_object_or_404(Adult, pk=id)

def commit(id, title, group):
    adult = Adult.objects.get(pk=id)
    adult.title = title
    adult.group = group
    adult.save()