from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client=Client()
        self.admin_user= get_user_model().objects.create_superuser(
            email='admin@abc.com',
            password='123456'
        )

        self.client.force_login(self.admin_user)
        self.user=get_user_model().objects.create_user(
            email='test@abc.com',
            password='1223',
            name='test user name'
        )

    def test_user_listed(self):
        '''test that user are listed in user page'''
        # core_user_changelist => {{ app_label }}_{{ model_name }}_changelist	 
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        '''tests the user edits page works'''
        url= reverse('admin:core_user_change', args=[self.user.id])
        res= self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        '''test that the user create page works'''
        url=reverse('admin:core_user_add')
        res=self.client.get(url)
        self.assertEqual(res.status_code, 200)

