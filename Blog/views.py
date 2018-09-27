from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView,TemplateView
from .forms import BlogForm, LoginForm, SignUpFrom
from .models import Blog
from django.urls import reverse, reverse_lazy
import uuid
from django.contrib import messages
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'next'


class HomePage(View):
    ctx = {'action': reverse_lazy('Blog:homepage'), 'id': 'home_page', 'button': 'Save and Done'}

    def get(self, request):
        form = BlogForm()
        return render(request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx})

    def post(self, request):
        form = BlogForm(request.POST)
        if form.is_valid():
            instance = form.save()
            if not request.user.is_authenticated:
                instance.secret_key = uuid.uuid4().hex[:6].upper()
                instance.save()
                url_path = reverse('Blog:homepage', kwargs={'id': instance.id, 'secret_key': instance.secret_key})
                messages.success(request, mark_safe("<a href='{url_path}'>{url_path}k</a>".format(url_path=url_path)))
                return redirect("Blog:Content", id=instance.id)
            else:
                instance.author = request.user
                instance.save()
                url_path = reverse('Blog:homepage', kwargs={'id': instance.id})
                messages.success(request, mark_safe("<a href='{url_path}'>{url_path}</a>".format(url_path=url_path)))
                return redirect("Blog:Content", id=instance.id)
        return render(request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx})


class ContentPage(View):
    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        soup = BeautifulSoup(blog.content, "lxml")
        list_of_contents = " "
        soup.body.hidden = True
        soup.html.hidden = True
        for tag in soup.body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            tag_text = tag.string
            index = int(tag.name[1])
            list_of_contents += "<ul>"*index + "<li>" + tag_text + "</li>"+"</ul>" * index
        return render(request, "Blog/content.html", {'blog': blog, 'blog_toc': list_of_contents})


class EditPage(View):
    ctx = {'id': 'edit_post', 'button': 'Edit and Save'}

    def get(self, request, id, secret_key=None):
        if secret_key is None:
            blog = get_object_or_404(Blog, id=id)
            form = BlogForm(instance=blog)
        else:
            blog = get_object_or_404(Blog, id=id, secret_key=secret_key)
            form = BlogForm(instance=blog)
        return render(request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx})

    def post(self, request, id, secret_key=None):
        if secret_key is None:
            blog = get_object_or_404(Blog, id=id)
            form = BlogForm(request.POST or None, instance=blog)
        else:
            blog = get_object_or_404(Blog, id=id, secret_key=secret_key)
            form = BlogForm(request.POST or None, instance=blog)
        if form.is_valid():
            instance = form.save()
            instance.save()
            messages.success(request, "Your post has been successfully Updated!!!")
            return redirect("Blog:Content", id=instance.id)
        return render(request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx})


class SignupView(CreateView):
    model = User
    form_class = SignUpFrom
    template_name = 'Blog/signup.html'
    success_url = reverse_lazy('Blog:login')


class LoginView(View):
    ctx = {'id': 'login_form', 'action': reverse_lazy('Blog:login'), 'button': 'LOGIN'}

    def get(self, request):
        form = LoginForm()
        return render(request, "Blog/login.html", {"form": form, 'ctx': self.ctx})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.get(username=username)
            if user is not None:
                if user.check_password(password):
                        if user.is_active:
                            login(request, user)
                            return redirect("Blog:homepage")
        return render(request, "Blog/login.html", {"form": form, 'ctx': self.ctx})


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect("Blog:homepage")


class ArticlesView(MyLoginRequiredMixin, TemplateView):
    template_name = "Blog/articles.html"

    def get_context_data(self, **kwargs):
        context = super(ArticlesView, self).get_context_data(**kwargs)
        context['articles'] = Blog.objects.filter(author=self.request.user)
        return context


