from .models import Blog
from django.contrib.auth.models import User
from django import forms
import bleach

VALID_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']


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

    def clean_content(self):
        content = self.cleaned_data['content']
        sanitized_content = bleach.clean(content, tags=['b', 'i', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        return sanitized_content


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class SignUpFrom(forms.ModelForm):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']
        if p1 != p2:
            raise forms.ValidationError("PASSWORD DOESNT MATCH")

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        user.save()
        return user












