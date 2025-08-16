from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment…'}), max_length=2000, help_text="Max 2000 characters.")

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        data = self.cleaned_data['content'].strip()
        if not data:
            raise forms.ValidationError("Comment cannot be empty.")
        return data