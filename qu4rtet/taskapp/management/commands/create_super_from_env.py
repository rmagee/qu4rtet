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

import environ
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = _('Will create a database and if the following '
             'environment variables are present and if the '
             'user represented by user and password have rights to '
             'create databases in the backend: POSTGRES_USER, '
             'POSTGRES_DB, POSTGRESS_PASSWORD, DATABASE_HOST, POSTGRES_HOST')

    def handle(self, *args, **options):
        print('Checking for environment variables...')
        env = self._read_env()
        username = env.str('DJANGO_SUPERUSER')
        user_pwd = env.str('DJANGO_SUPERUSER_PASSWORD')
        user_email = env.str('DJANGO_SUPERUSER_EMAIL')
        User.objects.create_user(
            username=username,
            password=user_pwd,
            email=user_email,
            is_super=True
        )
        print('User created.')

    def _read_env(self):
        ROOT_DIR = environ.Path(
            __file__) - 4
        env = environ.Env()
        READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=True)
        if READ_DOT_ENV_FILE:
            env_file = str(ROOT_DIR.path('.env'))
            env.read_env(env_file)
        EC2 = env.bool('EC2', False)
        if EC2:
            # look in the AWS parameter store for values
            from config.settings.ec2 import get_values
            get_values()
        return env
