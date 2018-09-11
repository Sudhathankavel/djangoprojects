from django.test import TestCase, Client
from .models import Blog
from .forms import BlogForm
from django.shortcuts import reverse


class FormFieldTest(TestCase):
    def setUp(self):
        self.post = Blog.objects.create(title='testBlogPost', content='test content')

    def test_fields_for_ten_character(self):
        form_data = {'title': 'test', 'content': 'content'}
        form = BlogForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_to_check_content_greater_than_title(self):
        data = {'title': 'testTitle With ten Characters', 'content': 'test content with TC'}
        form = BlogForm(data=data)
        self.assertFalse(form.is_valid())


class FormBlogTest(TestCase):
    def test_blog_form(self):
        client = Client(enforce_csrf_checks=True)
        request = self.client.post(reverse('Blog:homepage'), {'title': 'test Title With ten Characters', 'content': 'test content with TC'})
        error_data = 'content should be longer than title.'
        self.assertContains(request, error_data, status_code=200)



