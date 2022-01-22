from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL= reverse('user:create')
TOKEN_URL=reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

payload={
        'email':'test@abc.com',
        'password': '1234567890',
        'name': 'test name'
        }

payload_get_token={'email':payload['email'], 'password': payload['password']}


class PublicUserApiTest(TestCase):
    '''Tets the users API(public)'''
    def setUp(self) -> None:
        self.client = APIClient()

    def test_user_create_success(self):
        '''test creating user is successfully completed'''
       

        res=self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user=get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        '''test to check if user already exist'''
        
        create_user(**payload)
        res= self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_short(self):
        '''test to check if password is more than 5 char'''
        payload={
        'email':'test@abc.com',
        'password': '00',
         }
        res= self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exist)

    def test_create_token_user(self):
        '''test that a token is created for user'''
        create_user(**payload)
        res= self.client.post(TOKEN_URL, payload_get_token)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_invalid_credentials(self):
        '''test to check if token are created if invalid creds'''
        create_user(**payload)
        res= self.client.post(TOKEN_URL, payload_get_token)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ceate_token_no_user(self):
        '''test to check token not created if user doesnt exist'''
        res= self.client.post(TOKEN_URL, payload_get_token)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        '''test that email and password is required'''
        res= self.client.post(TOKEN_URL, {'ermail':'unknown', 'password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    

