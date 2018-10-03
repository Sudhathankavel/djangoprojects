from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView,TemplateView,DetailView
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
    login_url = reverse_lazy('Blog:login')
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
            if request.user.is_authenticated:
                instance.author = request.user
                instance.save()
            else:
                instance.secret_key = uuid.uuid4().hex[:6].upper()
                instance.save()
                url_path = reverse('Blog:editPage', kwargs={'id': instance.id, 'secret_key': instance.secret_key})
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
    ctx = {'id': 'edit_post', 'button': 'Edit and Save', 'claim_button': 'Claim'}

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get('secret_key'):
            self.blog = get_object_or_404(Blog, id=self.kwargs.get('id'), secret_key=self.kwargs.get('secret_key'))
        else:
            self.blog = get_object_or_404(Blog, id=self.kwargs.get('id'), author=request.user)
        return super(EditPage, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = BlogForm(instance=self.blog)
        if request.user.is_authenticated and self.blog.author is None:
            url = reverse('Blog:Claim', kwargs={'id': self.blog.id, 'secret_key': self.blog.secret_key})
            return redirect(url)
        else:
            return render(self.request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx,'blog':self.blog})

    def post(self, request, *args, **kwargs):
        form = BlogForm(self.request.POST or None, instance=self.blog)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return redirect("Blog:Content", id=instance.id)
        return render(self.request, "Blog/homepage.html", {'form': form, 'ctx': self.ctx})


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
            if user.check_password(password) and user.is_active:
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


class ClaimView(MyLoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'Blog/claim.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Blog, id=self.kwargs.get('id'), secret_key=self.kwargs.get('secret_key'))

    def dispatch(self, request, *args, **kwargs):
        self.blog = self.get_object()
        if not (request.user.is_authenticated and self.blog.author is None):
            raise Http404
        return super(ClaimView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        post.author = self.request.user
        post.secret_key = ''
        post.save()
        return redirect("Blog:Content", id=post.id)