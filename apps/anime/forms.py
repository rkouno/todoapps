from django import forms
from .models import Anime
from .models import Period
from django.contrib.admin.widgets import AdminDateWidget

class DateInput(forms.DateInput):
    input_type = 'date'

# セレクトボックス
class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
         return f"{obj.year} {obj.season}" # 表示したいカラム名を return

class AnimeForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = ('title', 'keyword', 'period', 'isEnd')
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder': 'Title', 
                    'class' : 'form-control'
                }),
            'keyword' : forms.TextInput(
                attrs={
                    'placeholder': 'Torrent keyword', 
                    'class' : 'form-control'
                }),
        }
    # セレクトボックス（期）  
    period = CustomModelChoiceField(
        queryset = Period.objects.all().order_by('-year','-period'),
        initial  = Period.objects.all().order_by('-id').first().id,
        widget   = forms.widgets.Select(attrs={'class':'form-select'}),
        
    )
    # セレクトボックス（放送ステータス）
    isEnd = forms.fields.ChoiceField(
        choices  = (('0','放送中'),('1','放送終了')),
        required = True, 
        label    = 'Status',
        initial  = 0, 
        widget   = forms.widgets.Select(attrs={'class':'form-select'})
    )