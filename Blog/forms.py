from .models import Blog
from django import forms


class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Blog
        fields = ["content", "title"]

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if len(content) < len(title):
            raise forms.ValidationError("content should be longer than title.")
