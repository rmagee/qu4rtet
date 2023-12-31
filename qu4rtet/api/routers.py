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
# Copyright 2018 SerialLab LLC.  All rights reserved.
from rest_framework import routers
from qu4rtet.api import viewsets

router = routers.DefaultRouter()

router.register(
    r'user',
    viewsets.UserViewSet,
    basename='users'
)
router.register(
    r'group',
    viewsets.GroupViewSet,
    basename='group'
)
router.register(
    r'permission',
    viewsets.PermissionViewSet,
    basename='permission'
)
router.register(
    r'read-only-users',
    viewsets.ReadOnlyUserViewSet,
    basename='read-only-users'
)
router.register(
    r'read-only-groups',
    viewsets.ReadOnlyGroupViewSet,
    basename='read-only-groups'
)

urlpatterns = router.urls
