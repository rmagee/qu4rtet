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
from django.contrib.admin import AdminSite
from quartet_epcis.models import entries
from quartet_epcis import admin

class Qu4rtetAdminSite(AdminSite):
    site_header = 'QU4RTET Administration'




admin_site = Qu4rtetAdminSite(name='qu4rtetadmin')

admin.register_to_site(admin_site)
