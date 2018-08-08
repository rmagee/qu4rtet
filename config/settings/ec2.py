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
import io
import boto3
from ec2_metadata import ec2_metadata

from logging import getLogger

logger = getLogger(__name__)


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.  The EC2 API only lets
    us ask for 10 at a time.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_user_data():
    """
    Looks in the EC2 user data for a name=value pair with a name of
    PARAMETER_GROUP and returns the value.  This is used to look up
    parameters in the EC2 parameter store.
    :return:
    """
    ret = None
    with io.StringIO(ec2_metadata.user_data.decode('utf-8')) as f:
        for line in f:
            vals = line.rstrip().split('=')
            if len(vals) == 2 and vals[0] == 'PARAMETER_GROUP':
                ret = vals[1].strip('\'"')
    return ret


def get_values():
    """
    Will look in the amazon parameter store for any env values that can be
    set.  The values in the store should have a prefix that is defined in
    user data of the EC2 instance as PARAMETER_GROUP=[group name].  For
    example:

        PARAMETER_GROUP=GROUP-1

    """
    found_parameters = {}
    parameter_group = get_user_data()
    if parameter_group:
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
            'ELASTIC_APM',
            'INTERNAL_IPS',
            'LOGGING_LEVEL',
        ]
        names = ['/%s/%s' % (parameter_group, name) for name in names]
        lists = list(chunks(names, 10))

        for name_list in lists:
            response = (client.get_parameters(
                Names=name_list,
                WithDecryption=True
            ))
            parameters = response.get('Parameters', {})
            for parameter in parameters:
                name = os.path.basename(parameter['Name'])
                os.environ[name] = parameter['Value']
                found_parameters[name] = parameter['Value']
                logger.info('Setting os.environ key %s to %s',
                            name, parameter['Value'])
    else:
        print('No parameter group was defined in the user-data.')

    # here we write out the value pairs to an env file if a bash
    # script needs to import into env variables in another process
    if len(found_parameters) > 0:
        with open('/tmp/q4_env', 'w+') as f:
            for k,v in found_parameters.items():
                f.write('%s=%s\n' % (k,v))

