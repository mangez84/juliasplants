from django.test import TestCase
from .models import Plant


class TestViews(TestCase):
    fixtures = ['testdata.json']

    def test_get_plants(self):
        """
        Test that the correct HTTP status code and template are returned.
        """
        response = self.client.get('/plants/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plants/plants.html')

    def test_get_plant_details(self):
        """
        Test that the correct HTTP status code and template are returned.
        """
        plant = Plant.objects.get(pk=1)
        response = self.client.get(f'/plants/{plant.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plants/plant_details.html')
