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
from quartet_epcis import admin as epcis_admin
from quartet_capture import admin as capture_admin
from list_based_flavorpack import admin as lbf_admin
from serialbox import admin as sb_admin
from quartet_output import admin as output_admin
from quartet_masterdata import admin as md_admin
from quartet_templates import admin as t_admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib import admin

class QuartetAdminSite(admin.AdminSite):
    site_header = "QU4RTET Administration"

class QUserAdmin(UserAdmin):
    list_filter = ()
    filter_horizontal = ()

admin_site = QuartetAdminSite(name='qu4rtetadmin')
admin_site.register(Group, GroupAdmin)
admin_site.register(User, QUserAdmin)

epcis_admin.register_to_site(admin_site)
capture_admin.register_to_site(admin_site)
lbf_admin.register_to_site(admin_site)
output_admin.register_to_site(admin_site)
md_admin.register_to_site(admin_site)
t_admin.register_to_site(admin_site)
sb_admin.register_to_site(admin_site)

try:
    from qu4rtet.local_admin import register_admins
    register_admins(admin_site)
except ImportError:
    print('No local_admin module detected.')
