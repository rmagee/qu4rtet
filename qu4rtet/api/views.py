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
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class APIRoot(APIView):
    '''
    Congratulations.  If you have arrived at this page, your QU4RTET
    system has been installed and is up and running.  This page and the
    browse-able API are for software developers looking to extend QU4RTET's
    features or to use the API layer for integration purposes.

    If you are an end user, get the QU4RTET UI per the instructions below.
    If you are a software developer, check the swagger and OpenAPI notes
    below.

    ## Get QU4RTET UI

    Get the QU4RTET UI client application to utilize the QU4RTET UI from
    an easy-to-use client interface.  See documentation and download
    instructions here:

    [https://gitlab.com/serial-lab/quartet-ui/](https://gitlab.com/serial-lab/quartet-ui/)

    Code is also available.

    ## OpenAPI/Swagger Information

    To enumerate all of the API options available on this QU4RTET
    instance, use the swagger or schema options below.

    The swagger option will expose all of the APIs available via
    a swagger UI interface.  If you'd like to generate a swagger
    schema to use for client generation and such, use the schema
    API to retrieve the schema.

    For more on Swagger and Open API see:

    ### Swagger
    [https://swagger.io/](https://swagger.io/)

    ### Open API Initiative
    [https://www.openapis.org/](https://www.openapis.org/)

    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response({
            'schema': reverse('schema', request=request, format=format),
            'swagger': reverse('swagger', request=request, format=format)
        })

    def get_view_name(self):
        return 'Schema API'
