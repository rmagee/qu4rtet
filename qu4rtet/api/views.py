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

class APIRoot(APIView):
    '''
    The schema exposed via this root API will output a swagger/OpenAPI
    definition of each of the APIs installed in on this QU4RTET system.

    For more on Swagger and Open API see:

    ## Swagger
    [https://swagger.io/](https://swagger.io/)

    ## Open API Initiative
    [https://www.openapis.org/](https://www.openapis.org/)

    '''
    def get(self, request, format=None):
        return Response({
            'schema': reverse('schema', request=request, format=format),
        })

    def get_view_name(self):
        return 'Schema API'
