from .models import Blog
from django import forms
from django.core.exceptions import ValidationError

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["content", "title"]


    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) < 10:
    #         raise ValidationError('title must contain atleast 10 characters')
    #     return title
    #
    # def clean_content(self):
    #     #import ipdb;ipdb.set_trace()
    #     content = self.cleaned_data['content']
    #     if len(content) < 10:
    #         raise ValidationError('content should contain atleast 10 characters')
    #     return content

    def clean(self):
        super().clean()
        title = self.cleaned_data.get("title")
        content = self.cleaned_data.get("content")
        if len(content) < len(title):
            raise forms.ValidationError("content should be longer than title.")
            return title
            return content
