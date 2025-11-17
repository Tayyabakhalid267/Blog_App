from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        Post.objects.create(text='just a test')

    def test_text_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.text}'
        self.assertEqual(expected_object_name, 'just a test')


class HomePageViewTest(TestCase):
    def setUp(self):
        # create a user and a post for tests
        self.user = User.objects.create_user(username='tester', password='pass')
        Post.objects.create(text='this is another test', author=self.user)

    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')

    def test_create_post_requires_login(self):
        # unauthenticated POST should redirect to login
        resp = self.client.post(reverse('home'), {'text': 'anon post'})
        self.assertIn(resp.status_code, (302, 301))

    def test_authenticated_user_can_create_edit_delete_post(self):
        # login
        self.client.login(username='tester', password='pass')
        # create
        resp = self.client.post(reverse('home'), {'text': 'a user post'})
        self.assertEqual(resp.status_code, 302)
        post = Post.objects.filter(text__icontains='a user post').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.author, self.user)
        # edit
        resp = self.client.post(reverse('post_edit', args=[post.pk]), {'text': 'edited text'})
        self.assertEqual(resp.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.text, 'edited text')
        # delete
        resp = self.client.post(reverse('post_delete', args=[post.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())
