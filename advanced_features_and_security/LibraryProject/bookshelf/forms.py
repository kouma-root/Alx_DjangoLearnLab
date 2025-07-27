from django import forms
from .models import Book

class BookForms(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']  # Include fields you want in the form

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter article title'}),
            'author': forms.Textarea(attrs={'placeholder': 'Enter author name '}),
            'publication_year': forms.NumberInput(attrs={'placeholder': 'Enter publication year'}),
        }
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)