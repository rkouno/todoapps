from django import forms

#model
from apps.anime.models import Adult
from apps.anime.models import Kana
from apps.anime.models import Category
from apps.book.models import Author
from apps.book.models import Series
from apps.book.models import Info

# セレクトボックス
class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
         return f"{obj.category}" # 表示したいカラム名を return
    
class AdultForm(forms.ModelForm):
    class Meta:
        model = Adult
        fields = ('title','group','category','score')
        widgets = {
            'title'    :forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title' }), 
            'group'    :forms.TextInput(attrs={'class':'form-control', 'placeholder':'Series' }), 
            'category' :forms.widgets.Select(attrs={'class':'form-select' }), 
            'score'    :forms.NumberInput(attrs={'class':'form-control', }), 
        }
    category = CustomModelChoiceField(
        queryset = Category.objects.all().order_by('slug'),
        widget   = forms.widgets.Select(attrs={'class':'form-select'}),
        
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category', 'kana', 'adult_flg')
        widgets = {
            'category' :forms.TextInput(attrs={'class':'form-control', 'placeholder':'Category' }), 
            'adult_flg' :forms.CheckboxInput(attrs={'class':'form-check-input', 'placeholder':'Adlut' }), 
        }
    kana = forms.ModelChoiceField(
        queryset = Kana.objects.all().order_by('id'),
        widget   = forms.widgets.Select(attrs={'class':'form-select'}),
    )

class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ('series_name','nyaa_keyword','status')
        widgets = {
            'series_name'  :forms.TextInput(attrs={'class':'form-control', 'placeholder':'series_name'}), 
            'nyaa_keyword' :forms.TextInput(attrs={'class':'form-control', 'placeholder':'nyaa_keyword'}), 
            'status'       :forms.widgets.Select(attrs={'class':'form-select' }), 
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"
        widgets = {
            'author_id'   :forms.TextInput(attrs={'class':'form-control', 'placeholder':'Author ID'}), 
            'author_name' :forms.TextInput(attrs={'class':'form-control', 'placeholder':'Author name'}), 
        }

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = "__all__"
        widgets = {
            'book_id'   : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Book ID'}),
            'genrue'    : forms.widgets.Select(attrs={'class':'form-select'}),
            'story_by'  : forms.widgets.Select(attrs={'class':'form-select'}),
            'art_by'    : forms.widgets.Select(attrs={'class':'form-select'}),
            'title'     : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
            'sub_title' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sub title'}),
            'series'    : forms.widgets.Select(attrs={'class':'form-select'}),
            'status'    : forms.widgets.Select(attrs={'class':'form-select'}),
            'save_path' : forms.widgets.Select(attrs={'class':'form-select'}),
        }
        series = forms.ModelChoiceField(
            queryset=Series.objects.none(), #空のクエリセット
            widget=forms.widgets.Select
        )