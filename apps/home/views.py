from django.shortcuts import render
import os
import ctypes

# Create your views here.
def home_list(request):
    return render(request, 'home/home_index.html',{})

def shutdown(request):
    #Windowsの終了
    os.system('shutdown -s -f')

def sleep(request):
    #Windowsの休止
    ctypes.windll.PowrProf.SetSuspendState(1, 1, 0)