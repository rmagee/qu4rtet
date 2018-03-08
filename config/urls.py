from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from rest_framework.schemas import get_schema_view
from qu4rtet.api.renderers import SwaggerRenderer
from qu4rtet.api.views import APIRoot
from rest_framework_swagger.views import get_swagger_view

schema_view = get_schema_view(title='QU4RTET API',
                               renderer_classes=[SwaggerRenderer])

swagger_view = get_swagger_view(title='QU4RTET API')
urlpatterns = [
                  # Django Admin, use {% url 'admin:index' %}
                  url(r'^$', APIRoot.as_view()),
                  url(r'^schema/', schema_view, name='schema'),
                  url(r'^swagger', swagger_view, name='swagger'),
                  url(settings.ADMIN_URL, admin.site.urls),
                  url(r'^manifest/', include('quartet_manifest.urls',
                                             namespace='manifest')),
                  url(r'^capture/', include('quartet_capture.urls',
                                            namespace='quartet-capture')),
                  url(r'^epcis/', include('quartet_epcis.urls')),
                  url(r'^api-auth/', include('rest_framework.urls')),
                  url(r'^rest-auth/', include('rest_auth.urls')),
                  url(r'^serialbox/', include('serialbox.api.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

registration = getattr(settings, 'ENABLE_REGISTRATION', None)

if registration:
    urlpatterns.append(url(r'^rest-auth/registration/',
                           include('rest_auth.registration.urls')))

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
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
                          url(r'^__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns
