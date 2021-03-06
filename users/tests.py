from django.shortcuts import reverse
from django.test import TestCase

from users.forms import UserCreateForm
from users.models import User

TEST_USER = {
    'username': 'Tester',
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'email': 'test@wp.pl',
}

TEST_SUPERUSER = {
    'username': 'SuperTester',
    'first_name': 'Super Name',
    'last_name': 'Last Name',
    'email': 'supertest@wp.pl',
}

PASSWORD = 'T3$tuser!@#$%^&*()'


class UserListViewTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username=TEST_SUPERUSER['username'],
                                                       email=TEST_SUPERUSER['email'],
                                                       password=PASSWORD)
        self.user = User.objects.create_user(username=TEST_USER['username'],
                                             email=TEST_USER['email'],
                                             password=PASSWORD)

    def test_list_view_template_used(self):
        self.client.login(username=self.superuser.email, password=PASSWORD)
        response = self.client.get(reverse('users:all'))
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_list_view_anonymous_user_redirects(self):
        response = self.client.get(reverse('users:all'))
        self.assertEqual(response.status_code, 302)

    def test_list_view_admin_sees_list(self):
        self.client.login(username=self.superuser.email, password=PASSWORD)
        response = self.client.get(reverse('users:all'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_logged_user_forbidden(self):
        self.client.login(username=self.user.email, password=PASSWORD)
        response = self.client.get(reverse('users:all'))
        self.assertEqual(response.status_code, 403)


class UserCreationTestCase(TestCase):
    def test_simple_creation(self):
        self.assertEqual(User.objects.all().count(), 0)
        User.objects.create()
        self.assertEqual(User.objects.all().count(), 1)

    def test_user_form_creates_user(self):
        self.assertEqual(User.objects.all().count(), 0)
        data = {**TEST_USER, **{'password1': PASSWORD, 'password2': PASSWORD}}
        new_user = UserCreateForm(data=data)
        new_user.save()

        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.first().username, 'Tester')

    def test_user_form_creates_user_not_trainer(self):
        data = {**TEST_USER, **{'password1': PASSWORD, 'password2': PASSWORD}}
        new_user = UserCreateForm(data=data)
        new_user.save()
        self.assertFalse(User.objects.first().trainer)

    def test_create_view_uses_user_form(self):
        response = self.client.get(reverse('users:create-form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_user_post_creates_user(self):
        response = self.client.post(reverse('users:create-form'),
                                    data={**TEST_USER, **{'password1': PASSWORD, 'password2': PASSWORD}})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.first().username, TEST_USER['username'])


class UserUpdateTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username=TEST_SUPERUSER['username'],
                                                       email=TEST_SUPERUSER['email'],
                                                       password=PASSWORD)
        self.user = User.objects.create_user(username=TEST_USER['username'],
                                             email=TEST_USER['email'],
                                             password=PASSWORD)

    def test_update_view_template_used(self):
        self.client.login(username=self.superuser.email, password=PASSWORD)
        response = self.client.get(reverse('users:update-form', kwargs={'pk': self.user.id}))
        self.assertTemplateUsed(response, 'users/user_form.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_update_view_anonymous_redirects_to_login(self):
        response = self.client.get(reverse('users:update-form', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_update_view_user_form_logged_user_forbidden(self):
        self.client.login(username=self.user.email, password=PASSWORD)
        response = self.client.get(reverse('users:update-form', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 403)

    def test_user_post_updates_user_forbidden(self):
        self.client.login(username=self.user.email, password=PASSWORD)
        response = self.client.post(reverse('users:update-form', kwargs={'pk': self.user.id}),
                                    {**TEST_USER, 'username': 'Alternative'})
        self.assertEqual(response.status_code, 403)

    def test_update_view_uses_user_form_admin(self):
        self.client.login(username=self.superuser.email, password=PASSWORD)
        response = self.client.get(reverse('users:update-form', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_user_post_updates_user_admin(self):
        self.client.login(username=self.superuser.email, password=PASSWORD)
        response = self.client.post(reverse('users:update-form', kwargs={'pk': self.user.id}),
                                    {**TEST_USER, 'username': 'Alternative'})
        self.assertEqual(response.status_code, 302)
        self.superuser.refresh_from_db()
        self.assertNotEqual(self.superuser.username, TEST_USER['username'])


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=TEST_USER['username'],
                                             email=TEST_USER['email'],
                                             password=PASSWORD)

    def test_template_used(self):
        self.client.login(username=self.user.email, password=PASSWORD)
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=TEST_USER['username'],
                                             email=TEST_USER['email'],
                                             password=PASSWORD)

    def test_template_used(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_post_data_email_as_username(self):
        response = self.client.post(reverse('login'), data={
            'username': TEST_USER['email'], 'password': PASSWORD
        })
        self.assertEqual(response.status_code, 302)

    def test_post_data_username_as_username_no_login(self):
        response = self.client.post(reverse('login'), data={
            'username': TEST_USER['username'], 'password': PASSWORD
        })
        self.assertEqual(response.status_code, 200)


class LogoutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=TEST_USER['username'],
                                             email=TEST_USER['email'],
                                             password=PASSWORD)

    def test_template_used(self):
        self.client.login(username=self.user.email, password=PASSWORD)
        response = self.client.get(reverse('logout'))
        self.assertTemplateUsed(response, 'users/logged_out.html')

    def test_if_user_can_logout(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        self.client.login(username=self.user.email, password=PASSWORD)
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

        self.client.get(reverse('logout'))
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)


class LoggedInOrLoggedOutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=TEST_USER['username'],
                                             email=TEST_USER['email'],
                                             password=PASSWORD)

    def test_not_logged_in_user_see_calendar_overview(self):
        self.client.login(username=self.user.email, password=PASSWORD)
        response = self.client.get(reverse('calendar:overview'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_see_user_related_site(self):
        self.client.login(username=self.user.email, password=PASSWORD)
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_anonymous_user_cannot_see_user_related_site(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
