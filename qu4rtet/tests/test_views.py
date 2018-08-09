# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.
import os
import django
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from qu4rtet.api.views import APIRoot

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.test'
django.setup()


class ViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345',
                                             is_superuser=True)
        login = self.client.login(username='testuser', password='12345')

    def test_root(self):
        url = 'http://localhost:8000'
        response = self.client.get(url)
        self.assertIs(response.status_code, 200)

    def test_schema(self):
        url = reverse('schema')
        response = self.client.get(url)
        self.assertIs(response.status_code, 200)

    def test_options(self):
        url = 'http://localhost:8000/user/'
        response = self.client.options(url)
        self.assertIs(response.status_code, 200)

    def test_group(self):
        url = 'http://localhost:8000/group/'
        response = self.client.options(url)
        self.assertIs(response.status_code, 200)

    def test_create_update_user(self):
        url = 'http://localhost:8000/user/'
        response = self.client.post(
            url,
            {
                'username': 'testuser2',
                'password': 'testuserpassword',
                'password2': 'testuserpassword',
                'email': 'testuser@serial-lab.local',
                'first_name': 'test user',
                'last_name': 'test'
            }
        )
        self.assertIs(response.status_code, 201)
        user_id = response.data['id']
        response = self.client.put(
            '{0}{1}/'.format(url, user_id),
            {
                'username': 'testuser2',
                'email': 'testuser@serial-lab.local',
                'first_name': 'test user',
                'last_name': 'test'
            }
        )
        self.assertIs(response.status_code, 200)

    def test_create_group(self):
        url = 'http://localhost:8000/group/'
        response = self.client.post(
            url,
            {'name': 'unit test group'}
        )
        self.assertIs(response.status_code, 201)

    def test_name(self):
        name = APIRoot().get_view_name()
        self.assertEqual('Schema API', name)
