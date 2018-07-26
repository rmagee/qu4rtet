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
from django.contrib.auth.password_validation import validate_password, \
    password_changed
from django.contrib.auth import models
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework import fields


class GroupSerializer(ModelSerializer):
    """
    Default serializer for the Group model.
    """

    class Meta:
        model = models.Group
        fields = '__all__'


class PermissionSerializer(ModelSerializer):
    """
    Default serializer for the Permission model.
    """

    class Meta:
        model = models.Permission
        fields = '__all__'


class UserSerializer(ModelSerializer):
    """
    Default serializer for the User model.
    """
    is_staff = fields.BooleanField(
        help_text=_('Whether or not this user can view other user info.')
    )
    password2 = fields.CharField(
        label=_('Confirm Password'),
        help_text=_('Please confirm your password.'),
        required=False,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = models.User
        fields = [
            'id',
            'password',
            'password2',
            'username',
            'first_name',
            'last_name',
            'email',
            'last_login',
            'date_joined',
            'is_staff',
            'is_active',
            'is_superuser',
            'groups',
            'user_permissions',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
                'required': False
            },
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True}
        }

    def validate(self, attrs):
        """
        Make sure the passwords are good if they were provided.
        """
        if attrs.get('password'):
            if attrs.get('password') != attrs.get('password2'):
                raise ValidationError(_('The passwords do not match.'))
        return attrs

    def create(self, validated_data):
        validate_password(validated_data.get('password'))
        user = models.User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            is_staff=validated_data.get('is_staff'),
            is_active=validated_data.get('is_active'),
            is_superuser=validated_data.get('is_superuser'),
        )
        user.groups.set(validated_data.get('groups'))
        user.user_permissions.set(validated_data.get('user_permissions'))
        return user

    def validate_password(self, password):
        """
        Check against the configured password validators.
        """
        validate_password(password)

    def update(self, instance: models.User, validated_data):
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.full_clean()
            instance.save()
            password_changed(password)
        return super().update(instance, validated_data)


class ReadOnlyPermissionSerializer(ModelSerializer):
    '''
    Default serializer for the Permission model.
    '''

    class Meta:
        model = models.Permission
        fields = [
            'id', 'name', 'codename'
        ]


class ReadOnlyGroupSerializer(ModelSerializer):
    permissions = ReadOnlyPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Group
        fields = ['id', 'name', 'permissions']


class ReadOnlyUserSerializer(ModelSerializer):
    """
    Default serializer for the ReadOnlyUser model.
    """
    groups = ReadOnlyGroupSerializer(many=True, read_only=True)
    user_permissions = ReadOnlyPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'last_login',
            'date_joined',
            'is_staff',
            'is_active',
            'is_superuser',
            'groups',
            'user_permissions',
        ]
        extra_kwargs = {'password': {'write_only': True}}
