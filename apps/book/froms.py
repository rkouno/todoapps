from django import forms
from apps.book.models import Workbook
from apps.book.models import Genrue
from apps.book.models import Book
from apps.book.models import Series

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
         return obj.genrue_name # 表示したいカラム名を return

class WorkBookForm(forms.ModelForm):
    # ジャンル
    genrue_name = CustomModelChoiceField(
        queryset   = Genrue.objects.all(),
    )

    class Meta:
        model = Workbook
        fields = ('genrue_name','story_by','art_by','title','sub_title','volume')

class BookForm(forms.ModelForm):
    # ジャンル
    genrue_name = CustomModelChoiceField(
        queryset=Genrue.objects.all(),
    )
    story_by  = forms.CharField(required=True)
    art_by    = forms.CharField(required=False)
    title     = forms.CharField(required=True)
    sub_title = forms.CharField(required=False)

    class Meta:
        model = Book
        fields = ('genrue_name','story_by','art_by','title','sub_title','volume',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
