import os
import requests
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
django.setup()


def create_default_user(instance_id):
    from django.contrib.auth.models import User
    username = 'qu4rtet-%s' % instance_id
    print('creating default user %s', username)
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username,
            'qu4rtet@serial-lab.local',
            instance_id
        )
        print('user %s was already in the system' % instance_id)


def get_instance_id():
    response = requests.get('http://169.254.169.254/latest/'
                            'meta-data/instance-id')
    return response.text


def create_launch_file(instance_id):
    directory_path = '/var/qu4rtet/'
    file_path = '%s%s' % (directory_path, instance_id)
    if os.path.exists(file_path):
        ret = False
    else:
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
    create_default_user(instance_id)
    create_launch_file(instance_id)
    print('complete.')


if __name__ == '__main__':
    run()
