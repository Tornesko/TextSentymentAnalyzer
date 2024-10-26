from django import forms
from .models import Text


class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('content', 'title')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Введите текст для анализа...'}),
        }
