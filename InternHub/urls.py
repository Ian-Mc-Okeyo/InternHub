from django.contrib import admin
from django.urls import path, include
#for media files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Intern.urls')),
    path('student/', include('student.urls')),
    path('company/', include('company.urls')),
]

if settings.DEBUG:#to enable serving of media files during development. Django cannot serve media files when debug=true
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
