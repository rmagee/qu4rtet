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
from django.utils.translation import gettext as _
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import exceptions
from qu4rtet.api import serializers


class BaseModelViewSet(ModelViewSet):
    """
    Base class for all of the viewsets in this module.  Sets default permission
    classes, etc.
    """
    permission_classes = (DjangoModelPermissions, IsAuthenticated)


class UserViewSet(BaseModelViewSet):
    """
    CRUD ready model view for the User model.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    search_fields = ['email', 'first_name', 'last_name', 'username']

    def check_permissions(self, request):
        super().check_permissions(request)
        if not request.user.has_perm('qu4rtet.read_users') and not \
            request.user.is_superuser and not request.user.is_staff and not \
            request.user.has_perm(
                'auth.change_user') and not request.user.has_perm(
            'auth.add_user'):
            raise exceptions.PermissionDenied(_('You do not have rights'
                                                ' to read user data.'))


class GroupViewSet(BaseModelViewSet):
    """
    CRUD ready model view for the Group model.
    """
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    search_fields = ['name', ]

    def check_permissions(self, request):
        super().check_permissions(request)
        if not request.user.has_perm('qu4rtet.read_groups') and not \
            request.user.is_superuser and not request.user.is_staff and not \
            request.user.has_perm('auth.change_group'):
            raise exceptions.PermissionDenied(_('You do not have rights'
                                                ' to read group data.'))


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

    def check_permissions(self, request):
        super().check_permissions(request)
        if not request.user.has_perm('qu4rtet.read_users') and not \
            request.user.is_superuser and not request.user.is_staff and not \
            request.user.has_perm(
                'auth.change_user') and not request.user.has_perm(
            'auth.add_user'):
            raise exceptions.PermissionDenied(_('You do not have rights'
                                                ' to read user data.'))

    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)


class ReadOnlyGroupViewSet(ReadOnlyModelViewSet):
    """
    Read only model view set for the Group model.
    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = models.Group.objects.all()
    serializer_class = serializers.ReadOnlyGroupSerializer
    search_fields = ['name', ]

    def check_permissions(self, request):
        super().check_permissions(request)
        if not request.user.has_perm('qu4rtet.read_groups') and not \
            request.user.is_superuser and not request.user.is_staff and not \
            request.user.has_perm(
                'auth.change_group') and not request.user.has_perm(
            'auth.add_group'):
            raise exceptions.PermissionDenied(_('You do not have rights'
                                                ' to read group data.'))
