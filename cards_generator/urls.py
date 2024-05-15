from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from generator.views import home

urlpatterns = ([
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('generator/', include('generator.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
