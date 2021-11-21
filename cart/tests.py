from django.test import TestCase


class TestViews(TestCase):
    def test_get_cart(self):
        """
        Test that the correct HTTP status code and template are returned.
        """
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
