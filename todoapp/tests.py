from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password'
        }
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        User.objects.create_user(username='testuser', password='password')
        data = {
            'username': 'testuser',
            'password': 'password'
        }
        response = self.client.post('/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_todo_list(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=user)
        response = self.client.get('/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_todo_item(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=user)
        data = {
            'todo_name': 'Test ToDo',
            'description': 'Test description',
            'status': False
        }
        response = self.client.post('/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

