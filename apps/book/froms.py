from django import forms
from .models import Workbook,genrue,book

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
         return obj.genrue_name # 表示したいカラム名を return

class WorkBookForm(forms.ModelForm):
    genrue_name = CustomModelChoiceField(
        queryset=genrue.objects.all()
    )

    class Meta:
        model = Workbook
        fields = ('genrue_name','story_by','art_by','title','sub_title','volume',)

class BookForm(forms.ModelForm):
    genrue_name = CustomModelChoiceField(
        queryset=genrue.objects.all()
    )

    class Meta:
        model = book
        fields = ('genrue_name','story_by','art_by','title','sub_title','volume',)
