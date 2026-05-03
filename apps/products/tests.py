from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductTests(APITestCase):
    def setUp(self):
        self.merchant = self.create_merchant()
        self.product_data = {
            "name": "Test Product",
            "price": 99.99,
            "description": "A test product",
            "stock": 10,
        }

    def create_merchant(self):
        
        return User.objects.create_user(
            email="merchant@example.com",
            username="merchant",
            password="password123",
            role="merchant"
        )
    
    def test_create_product(self):
        self.client.force_authenticate(user=self.merchant)
        url = reverse('create-product')
        response = self.client.post(url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get().name, "Test Product")