from django import forms

#model
from apps.anime.models import Adult
from apps.book.models import Author
from apps.book.models import Series
from apps.book.models import Info

class AdultForm(forms.ModelForm):
    class Meta:
        model = Adult
        fields = ('title','group')
        widgets = {
            'title' :forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title' }), 
            'group' :forms.TextInput(attrs={'class':'form-control', 'placeholder':'Series' }), 
        }
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