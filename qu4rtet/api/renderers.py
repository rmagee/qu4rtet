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
from rest_framework import renderers
from rest_framework_swagger.renderers import OpenAPIRenderer


class SwaggerRenderer(renderers.BaseRenderer):
    '''
    Used to render out the API as a swagger schema.
    '''
    media_type = 'application/openapi+json'
    format = 'swagger'


class JSONOpenAPIRenderer(OpenAPIRenderer):
    '''
    Swagger-js sends the Accept header as application/json by default.
    See: https://github.com/marcgibbons/django-rest-swagger/issues/701
    '''
    media_type = 'application/json'
