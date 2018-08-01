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
from django.contrib.auth.models import Permission, ContentType, User, Group
from django.db.utils import ProgrammingError

try:
    ct = ContentType.objects.get_for_model(User)
    can_read_users, created = Permission.objects.get_or_create(
        codename='read_users',
        content_type=ct
    )
    if created:
        can_read_users.name = 'Can read user data.'
        can_read_users.save()

    ct = ContentType.objects.get_for_model(Group)
    can_read_groups, created = Permission.objects.get_or_create(
        codename='read_groups',
        content_type=ct
    )
    if created:
        can_read_groups.name = 'Can read group data.'
        can_read_groups.save()
except ProgrammingError:
    # for the first database migration, this will fail- but doesn't matter
    pass
