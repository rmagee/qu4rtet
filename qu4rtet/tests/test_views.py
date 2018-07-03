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
from django.urls import reverse
from django.contrib.auth.models import User

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.test'
django.setup()

class ViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        login = self.client.login(username='testuser', password='12345')

    def test_root(self):
        url = 'http://localhost:8000'
        response = self.client.get(url)
        self.assertIs(response.status_code, 200)

    def test_schema(self):
        url = reverse('schema')
        response = self.client.get(url)
        self.assertIs(response.status_code, 200)

    def test_swagger(self):
        url = reverse('swagger')
        response = self.client.get(url)
        self.assertIs(response.status_code, 200)

