from django.test import TestCase


class TestViews(TestCase):

    def test_get_home(self):
        """
        Test that the correct HTTP status code and template are returned.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
