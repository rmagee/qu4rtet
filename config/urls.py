from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path
from django.views import defaults as default_views
from rest_framework.schemas import get_schema_view
from qu4rtet.api.renderers import JSONOpenAPIRenderer
from qu4rtet.api import routers
from qu4rtet.api.views import APIRoot
from rest_framework import permissions
from drf_yasg.views import get_schema_view as yasg_get_shemea_view
from drf_yasg import openapi

from quartet_trail.urls import urlpatterns as trail_patterns

schema_view = get_schema_view(title='QU4RTET API',
                              renderer_classes=[JSONOpenAPIRenderer])

yasg_schema_view = yasg_get_shemea_view(
   openapi.Info(
      title="QU4RTET API",
      default_version='v1',
      description="The QU4RTET API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
                  url(r'^$', APIRoot.as_view()),
                  url(r'^schema/?', schema_view, name='schema'),
                  url(r'^swagger(?P<format>\.json|\.yaml)$', yasg_schema_view.without_ui(cache_timeout=0), name='schema-json'),
                  url(r'^swagger/$', yasg_schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
                    url(r'^redoc/$', yasg_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  url(r'^manifest/', include('quartet_manifest.urls',
                                             namespace='manifest')),
                  url(r'^capture/', include('quartet_capture.urls',
                                            namespace='quartet-capture')),
                  url(r'^output/', include('quartet_output.urls',
                                            namespace='quartet-output')),
                  url(r'^accounts/', include('allauth.urls')),
                  url(r'^epcis/', include('quartet_epcis.urls')),
                  url(r'^api-auth/', include('rest_framework.urls')),
                  url(r'^rest-auth/', include('rest_auth.urls')),
                  url(r'^serialbox/', include('serialbox.api.urls')),
                  url(r'^masterdata/', include('quartet_masterdata.urls')),
                  url(r'^templates/', include('quartet_templates.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += routers.urlpatterns
urlpatterns += trail_patterns
try:
    from .local_urls import urlpatterns as local_urlpatterns
    urlpatterns += local_urlpatterns
    print('LOCAL URLS FOUND')
except ImportError:
    print('NO LOCAL URLS FOUND')

registration = getattr(settings, 'ENABLE_REGISTRATION', False)

if registration:
    urlpatterns.append(url(r'^rest-auth/registration/',
                           include('rest_auth.registration.urls')))
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from qu4rtet.admin import admin_site
    urlpatterns = [
        path(getattr(settings, 'DJANGO_ADMIN_URL', 'qu4rtetadmin/'), admin_site.urls),
    ] + urlpatterns

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]

    try:
        if 'debug_toolbar' in settings.INSTALLED_APPS:
            import debug_toolbar

            urlpatterns = [
                              url(r'^__debug__/', include(debug_toolbar.urls)),
                          ] + urlpatterns
    except ImportError:
        print('Could not import the debug toolbar.')
