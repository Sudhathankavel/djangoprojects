from django.test import TestCase, Client
from .models import Blog ,User
from .forms import BlogForm
from django.shortcuts import reverse
import uuid


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
        data = '/{id}/edit/{secret_key}'.format(id=instance.id, secret_key=instance.secret_key)
        self.assertContains(response, data, status_code=200)
        content_response = self.client.get(reverse('Blog:Content', kwargs={'id': instance.id}))
        self.assertNotContains(content_response, data, status_code=200)


class EditLinkTest(TestCase):

    def setUp(self):
        self.blogpost = Blog.objects.create(title='test blog post with ORM', content='test content by a post with ORM')
        self.blogpost.secret_key = uuid.uuid4().hex[:6].upper()
        self.blogpost.save()
        self.instance = Blog.objects.get(title='test blog post with ORM')

    def test_verify_redirection_of_edit_link(self):
        response = self.client.get(reverse('Blog:editPage', kwargs={'id': self.instance.id, 'secret_key': self.instance.secret_key}))
        self.assertContains(response, 'test blog post with ORM', status_code=200)
        wrong_secret_key = 'DF20192'
        response = self.client.get(reverse('Blog:editPage', kwargs={'id': self.instance.id, 'secret_key': wrong_secret_key}))
        self.assertEquals(response.status_code, 404)

    def test_changes_edits_the_post_successfully(self):
        update_data = {'title': 'test title to check the updation', 'content': 'test content to check the updation is working'}
        response = self.client.post(reverse('Blog:editPage', kwargs={'id': self.instance.id, 'secret_key': self.instance.secret_key}), update_data, follow=True)
        fetch_updated_data = Blog.objects.get(title='test title to check the updation')
        self.assertEquals(fetch_updated_data.content, 'test content to check the updation is working' )

    def test_rendering_newLine_as_brk(self):
        response = self.client.post(reverse('Blog:homepage'), {'title': 'ANONYMOUS BLOG POST RENDERING NEW LINES AS BREAK', 'content': 'hai I am using Django for development,\n when I render it to a template should  show the newline character'}, follow=True)
        self.assertContains(response, 'I am using Django for development,<br /> when I render it to a template should  show the newline character', status_code=200)


class RenderingTest(TestCase):

    def test_to_check_rendering_of_unsafe_tags(self):
        content_to_render = {'title': 'ANONYMOUS BLOG POST RENDERING', 'content': '<h1>This is h1 tag</h1><script>this is nonsafe tag</script>\n\n<h3>And this is h3 tag</h3>'}
        response = self.client.post(reverse('Blog:homepage'), content_to_render, follow=True)
        self.assertContains(response, '<h1>This is h1 tag</h1>', status_code=200)
        self.assertContains(response, '&lt;script&gt;this is nonsafe tag&lt;/script&gt;', status_code=200)

    def test_to_check_outline(self):
        content = {'title': 'ANONYMOUS BLOG POST - OULTINE CHECK', 'content': '<h1>This is h1 tag</h1><h2>This is h2 tag</h2>'}
        response = self.client.post(reverse('Blog:homepage'), content, follow=True)
        self.assertContains(response, '<ul><li>This is h1 tag</li></ul><ul><ul><li>This is h2 tag</li></ul></ul></p>', status_code=200)


class UserDataTestClass(TestCase):
    def setUp(self):
        self.user_data = {'username': 'foo', 'email': 'foo@gmail.com', 'password': 'testuser'}
        User.objects.create_user(**self.user_data)


class SignupLoginUsersTest(UserDataTestClass):

    def test_signup_with_wrong_password(self):
        response = self.client.post(reverse('Blog:signup'), {'username': 'foo', 'email': 'foo@gmail.com', 'password1': 'testuser', 'password2': 'Testuser'}, follow=True)
        self.assertFalse(response.context['user'].is_active)
        self.assertContains(response, "PASSWORD DOESNT MATCH", status_code=200)

    def test_signup_with_existing_username(self):
        response = self.client.post(reverse('Blog:signup'), {'username': 'foo', 'email': 'foo@gmail.com', 'password1': 'testuser', 'password2': 'testuser'}, follow=True)
        self.assertFalse(response.context['user'].is_active)
        self.assertContains(response, "A user with that username already exists.", status_code=200)

    def test_signup_with_valid_data(self):
        response = self.client.post(reverse('Blog:signup'), {'username': 'foo2', 'email': 'foo@gmail.com', 'password1': 'testuser', 'password2': 'testuser'}, follow=True)
        self.assertRedirects(response, reverse('Blog:login'), status_code=302, target_status_code=200)

    def test_login_with_invalid_password(self):
        response = self.client.post(reverse('Blog:login'), {'username': 'foo', 'password': 'Testuser'}, follow=True)
        self.assertContains(response, "Wrong password", status_code=200)

    def test_login_unregistered_user(self):
        response = self.client.post(reverse('Blog:login'), {'username': 'testuser', 'password': 'secret'}, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_login_registered_user(self):
        response = self.client.post(reverse('Blog:login'), self.user_data, follow=True)
        self.assertTrue(response.context['user'].is_active)

