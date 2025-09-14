from django.test import TestCase
from django.urls import reverse
from .models import Product

class ProductTests(TestCase):
    def setUp(self):
        Product.objects.create(title='Test Product', description='Desc', price='9.99', stock=10, slug='test-product')

    def test_product_list(self):
        resp = self.client.get(reverse('store:product_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Product')

    def test_product_detail(self):
        resp = self.client.get(reverse('store:product_detail', args=['test-product']))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Product')
