from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

                       url(r'^', include('multitest.urls')),
                       url(r'^admin/', include('multitest_admin.urls', 'admin')),
                       url(r'^inplaceeditform/', include('inplaceeditform.urls')),


                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)