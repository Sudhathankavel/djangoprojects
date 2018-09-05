from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import BlogForm
from .models import Blog
from django.urls import reverse, reverse_lazy
import uuid
from django.contrib import messages
from django.utils.safestring import mark_safe


class HomePage(View):
    ctx = {'action': reverse_lazy('Blog:homepage'), 'id': 'home_page', 'button': 'Save and Done'}

    def get(self, request):
        form = BlogForm()
        return render(request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx})

    def post(self, request):
        form = BlogForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.secret_key = uuid.uuid4().hex[:6].upper()
            instance.save()
            url_path = reverse('Blog:homepage', kwargs={'id': instance.id, 'secret_key': instance.secret_key})
            messages.success(request, mark_safe("<a href='{url_path}'>{url_path}k</a>".format(url_path=url_path)))
            return redirect("Blog:Content", id=instance.id)
        return render(request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx})


class ContentPage(View):
    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        return render(request, "Blog/content.html", {'blog': blog})


class EditPage(View):
    ctx = {'id': 'edit_post', 'button': 'Edit and Save'}

    def get(self, request, id, secret_key):
        blog = get_object_or_404(Blog, id=id, secret_key=secret_key)
        form = BlogForm(instance=blog)
        return render(request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx})

    def post(self, request, id, secret_key):
        blog = get_object_or_404(Blog, id=id, secret_key=secret_key)
        form = BlogForm(request.POST or None, instance=blog)
        if form.is_valid():
            instance = form.save()
            instance.save()
            messages.success(request, "Your post has been successfully Updated!!!")
            return redirect("Blog:Content", id=instance.id)
        return render(request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx})