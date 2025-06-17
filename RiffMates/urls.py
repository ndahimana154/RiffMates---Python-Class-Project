from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from home import views as home_views
from content import views as content_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_views.homepage, name="home"),
    path("accounts/", include('django.contrib.auth.urls')),
    path('credits/', home_views.credits, name="credits"),
    path('about/', home_views.about, name="about"),
    path('news/', home_views.news, name='news'),
    path('band/', include('band.urls')), 
    path('content/',include('content.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)