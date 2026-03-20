from .models import Articles
from django.forms import ModelForm, TextInput, DateInput, Textarea, Select, HiddenInput


class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'intro', 'content', 'category']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'What would you like to discuss?'
            }),
            'intro': TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Write the intro'
            }),
            'content': Textarea(attrs={
                'class': 'textarea',
                'placeholder': 'Share your thoughts, ask questions, or start a discussion...',
                'rows': 12
            }),
            'category': HiddenInput(attrs={'id': 'hiddenCategoryInput'}),
        }

