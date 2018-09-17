from .models import Blog
from django import forms
from bs4 import BeautifulSoup


VALID_TAGS = ['b', 'i', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']


class BlogForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'content'}))

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

    def clean_title(self):
        title = self.cleaned_data.get("title")
        soup = BeautifulSoup(title, features="html5lib")
        for tag in soup.findAll(True):
            if tag.name not in VALID_TAGS:
                tag.hidden = True
        return soup.renderContents().decode("utf-8")

    def clean_content(self):
        content = self.cleaned_data.get("content")
        soup = BeautifulSoup(content, features="html5lib")
        for tag in soup.findAll(True):
            if tag.name not in VALID_TAGS:
                tag.hidden = True
        return soup.renderContents().decode("utf-8")