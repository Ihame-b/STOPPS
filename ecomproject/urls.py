from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ecomapp import views as map_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("ecomapp.urls")),
    
] 

# Serve static and media files in development only
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
