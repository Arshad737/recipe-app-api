from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating user with email was successful"""
        email='arshadkhan@gmail.com'
        password='password'
        user=get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_nomalised(self):
        '''test the email for a new user is normalised'''
        email='test@AJHA.com'
        user= get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''test if email is invalid'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_super_user_is_created(self):
        '''Test creating a new super user'''
        user= get_user_model().objects.create_superuser(
            'test@abc.com',
            'password'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
