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
        self.assertEqual(len(form.errors), 2)
        self.assertEquals(form.errors['title'], ['Ensure this value has at least 10 characters (it has 4).'])
        self.assertEquals(form.errors['content'], ['Ensure this value has at least 10 characters (it has 7).'])

    def test_to_check_content_greater_than_title(self):
        data = {'title': 'testTitle With ten Characters', 'content': 'test content with TC'}
        form = BlogForm(data=data)
        # import pdb;pdb.set_trace()
        self.assertEqual(len(form.errors), 1)
        self.assertEquals(form.errors['__all__'], ['content should be longer than title.'])


class FormBlogTest(TestCase):
    def setUp(self):
        self.form_data = {'title': 'test Title With ten Characters', 'content': 'test content with Ten Characters long'}

    def test_blog_form(self):
        client = Client(enforce_csrf_checks=True)
        response = self.client.post(reverse('Blog:homepage'), {'title': 'test Title With ten Characters long', 'content': 'test content with TC'})
        error_data = 'content should be longer than title.'
        self.assertContains(response, error_data, status_code=200)

    def test_verify_redirect(self):
        response = self.client.post(reverse('Blog:homepage'), self.form_data)
        instance = Blog.objects.get(title='test Title With ten Characters')
        self.assertRedirects(response, reverse('Blog:Content', kwargs={'id': instance.id}), status_code=302, target_status_code=200)

    def test_redirected_page_is_in_html(self):
        response = self.client.post(reverse('Blog:homepage'), self.form_data, follow=True)
        self.assertContains(response, 'test Title With ten Characters', status_code=200)
        self.assertContains(response, 'test content with Ten Characters long', status_code=200)

    def test_verify_edit_link_correct_on_first_fetch_incorrect_on_sec_fetch(self):
        response = self.client.post(reverse('Blog:homepage'), self.form_data, follow=True)
        instance = Blog.objects.get(title='test Title With ten Characters')
        data = '/Blog/{id}/edit/{secret_key}'.format(id=instance.id, secret_key=instance.secret_key)
        self.assertContains(response, data, status_code=200)
        content_response = self.client.get(reverse('Blog:Content', kwargs={'id': instance.id}))
        self.assertNotContains(content_response, data, status_code=200)








