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
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth import models
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from qu4rtet.api import serializers


class BaseModelViewSet(ModelViewSet):
    """
    Base class for all of the viewsets in this module.  Sets default permission
    classes, etc.
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions)


class UserViewSet(BaseModelViewSet):
    """
    CRUD ready model view for the User model.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    search_fields = ['email', 'first_name', 'last_name', 'username']


class GroupViewSet(BaseModelViewSet):
    """
    CRUD ready model view for the Group model.
    """
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    search_fields = ['name', ]


class PermissionViewSet(BaseModelViewSet):
    """
    CRUD ready model view for the Permission model.
    """
    queryset = models.Permission.objects.all()
    serializer_class = serializers.PermissionSerializer
    search_fields = ['name', ]


class ReadOnlyUserViewSet(ReadOnlyModelViewSet):
    """
    Read-only ready model view for the User model.
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = models.User.objects.all()
    serializer_class = serializers.ReadOnlyUserSerializer
    search_fields = ['email', 'first_name', 'last_name', 'username']


class ReadOnlyGroupViewSet(ReadOnlyModelViewSet):
    """
    Read only model view set for the Group model.
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = models.Group.objects.all()
    serializer_class = serializers.ReadOnlyGroupSerializer
    search_fields = ['name', ]
