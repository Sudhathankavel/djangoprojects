from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import BlogForm
from .models import Blog
import uuid


class HomePage(View):
    def get(self, request):
        form = BlogForm()
        return render(request, "Blog/homepage.html", {'form': form})

    def post(self, request):
        form = BlogForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.secret_key = uuid.uuid4().hex[:6].upper()
            instance.save()
            return redirect("Blog:Content", id=instance.id)
        return render(request, "Blog/homepage.html", {'form': form})


class ContentPage(View):
    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        return render(request, "Blog/content.html", {'blog': blog})
