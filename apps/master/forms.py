from django import forms

#model
from apps.anime.models import Adult

class AdultForm(forms.ModelForm):
    class Meta:
        model = Adult
        fields = ('title','group')
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'placeholder': 'Title', 
                    'class' : 'form-control'
                }),
            'group' : forms.TextInput(
                attrs={
                    'placeholder': 'Series', 
                    'class' : 'form-control'
                }),
        }