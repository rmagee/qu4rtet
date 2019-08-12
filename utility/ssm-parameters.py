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

import boto3
import random
import click

SECRET_KEY = ''.join([random.SystemRandom().choice(
    'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

keys = [
    ('/{0}/DATABASE_HOST', 'String', 'localhost'),
    ('/{0}/DJANGO_AWS_ACCESS_KEY_ID', 'String', 'Provide Value'),
    ('/{0}/DJANGO_AWS_SECRET_ACCESS_KEY', 'SecureString', 'Provide Value'),
    ('/{0}/DJANGO_AWS_STORAGE_BUCKET_NAME', 'String', 'Provide Value'),
    ('/{0}/DJANGO_DEBUG', 'String', 'False'),
    ('/{0}/DJANGO_SECRET_KEY', 'SecureString', SECRET_KEY),
    ('/{0}/DJANGO_SENTRY_DSN', 'String', 'Provide Value'),
    ('/{0}/DJANGO_SETTINGS_MODULE', 'String', 'config.settings.production'),
    ('/{0}/DJANGO_SUPERUSER', 'SecureString', 'Provide Value'),
    ('/{0}/DJANGO_SUPERUSER_EMAIL', 'String', 'Provide Value'),
    ('/{0}/DJANGO_SUPERUSER_PASSWORD', 'SecureString', 'Provide Value'),
    ('/{0}/LOGGING_LEVEL', 'String', 'WARNING'),
    ('/{0}/POSTGRES_DB', 'String', 'qu4rtet'),
    ('/{0}/POSTGRES_PASSWORD', 'SecureString', 'Provide Value'),
    ('/{0}/USE_AWS', 'String', 'False'),
    ('/{0}/USE_SENTRY', 'String', 'False'),
    ('/{0}/DJANGO_ENABLE_ADMIN', 'String', 'True'),
]


@click.command()
@click.option("--group_name", help="The Parameter Group name you'd like to "
                                   "create.")
@click.option("--overwrite", default=False,
              help="Whether or not to overwrite an existing group's values"
                   " with the same name as group_name.")
def create_parameters(group_name, overwrite=False):
    client = boto3.client(
        'ssm'
    )

    for key in keys:
        client.put_parameter(
            Name=key[0].format(group_name),
            Description='Parameter Group %s %s value.' % (group_name, key[0]),
            Value=key[2],
            Type=key[1],
            Overwrite=bool(overwrite)
        )

if __name__ == '__main__':
    create_parameters()
