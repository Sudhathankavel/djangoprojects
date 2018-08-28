from django.shortcuts import render, redirect
from django.views import View
from .forms import BlogForm
from django import forms
from .models import Blog
import uuid
# Create your views here.


class HomePage(View):
    def get(self, request):
        form = BlogForm()
        return render(request, "Blog/homepage.html", {'form': form})

    def post(self, request):
        # import pdb;pdb.set_trace()
        # form = BlogForm(request.POST, request.FILES)
        # if form.is_valid():
        #     instance = form.save(commit=False)
        #     instance.secret_key = "key"
        #     instance.save()
        form = BlogForm(request.POST)
        if form.is_valid():
            #import pdb;pdb.set_trace()
            instance = form.save()
            instance.secret_key = uuid.uuid4().hex[:6].upper()
            instance.save()
            return redirect("Blog:Content", id=instance.id)
        return render(request, "Blog/homepage.html", {'form': form})


class ContentPage(View):
    def get(self, request, id):
        blog = Blog.objects.filter(id=id)
        return render(request, "Blog/content.html", {'blog': blog})
