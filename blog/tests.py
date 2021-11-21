from django.test import TestCase
from .models import BlogPost


class TestViews(TestCase):
    fixtures = ['testdata.json']

    def test_get_blog_posts(self):
        """
        Test that the correct HTTP status code and template are returned.
        """
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_posts.html')

    def test_get_blog_post_details(self):
        """
        Test that the correct HTTP status code and template are returned.
        """
        blog_post = BlogPost.objects.get(pk=1)
        response = self.client.get(f'/blog/{blog_post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_details.html')
