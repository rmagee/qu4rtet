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
import boto3
from ec2_metadata import ec2_metadata

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_values():
    client = boto3.client(
        'ssm',
        region_name=ec2_metadata.region
    )
    names = [
        'DJANGO_DEBUG',
        'DJANGO_EMAIL_BACKEND',
        'DATABASE_HOST',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'POSTGRES_PORT',
        'POSTGRES_DB',
        'DJANGO_ADMIN_URL',
        'CONN_MAX_AGE',
        'DJANGO_SETTINGS_MODULE',
        'DJANGO_SECRET_KEY',
        'DJANGO_ALLOWED_HOSTS',
        'DJANGO_DEBUG',
        'DJANGO_AWS_ACCESS_KEY_ID',
        'DJANGO_AWS_SECRET_ACCESS_KEY',
        'DJANGO_AWS_STORAGE_BUCKET_NAME',
        'DJANGO_MAILGUN_API_KEY',
        'DJANGO_SERVER_EMAIL',
        'MAILGUN_SENDER_DOMAIN',
        'USE_SENTRY',
        'DJANGO_SENTRY_DSN',
        'CELERY_BROKER_URL',
        'USE_AWS',
        'LOGGING_PATH',
        'HTTPS_ONLY',
        'DJANGO_SUPERUSER',
        'DJANGO_SUPERUSER_PASSWORD',
        'DJANGO_SUPERUSER_EMAIL',
        'ELASTIC_APM'
    ]
    names = ['/%s/%s' % (ec2_metadata.private_ipv4, name) for name in names]
    print(names)
    lists = list(chunks(names,10))

    for list in lists:
        response = (client.get_parameters(
            Names=list,
            WithDecryption=True
        ))
        parameters = response.get('Parameters', {})
        for parameter in parameters:
            name = os.path.basename(parameter['Name'])
            print('setting %s to %s' % (name, parameter['Value']))
            print(name)
            os.environ[name] = parameter['Value']
