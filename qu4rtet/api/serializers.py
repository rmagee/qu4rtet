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
from django.contrib.auth import models
from rest_framework.serializers import ModelSerializer, CharField


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

    class Meta:
        model = models.User
        fields = [
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
