import os
import sys
import requests
import django

quartet_path = '/srv/qu4rtet'
try:
    sys.path.index(quartet_path)  # Or os.getcwd() for this directory
except ValueError:
    sys.path.append(quartet_path)  # Or os.getcwd() for this directory
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
django.setup()


def create_default_user(instance_id, reservation_id):
    from django.contrib.auth.models import User
    username = 'qu4rtet-%s' % reservation_id
    print('creating default user %s' % username)
    if not User.objects.filter(username=username).exists():
        User.objects.filter(username__startswith='qu4rtet-').delete()
        User.objects.create_superuser(
            username,
            'qu4rtet@serial-lab.local',
            instance_id
        )
        print('user %s was created in the system' % username)


def get_instance_id():
    response = requests.get('http://169.254.169.254/latest/'
                            'meta-data/instance-id')
    return response.text

def get_reservation_id():
    response = requests.get('http://169.254.169.254/latest/'
                            'meta-data/reservation-id')
    return response.text

def create_launch_file(instance_id):
    directory_path = '/var/quartet/'
    file_path = '%s%s' % (directory_path, instance_id)
    if os.path.exists(file_path):
        ret = False
    else:
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        print('Creating instance id file.')
        with open(file_path, 'w') as f:
            f.write(instance_id)
            f.close()
        print('Created')
        ret = True
    return ret


def run():
    instance_id = get_instance_id()
    reservation_id = get_reservation_id()
    file_created = create_launch_file(instance_id)
    if file_created:
        create_default_user(instance_id, reservation_id)
    print('complete.')


if __name__ == '__main__':
    run()
