from django.contrib import admin
from django.urls import path,include
from home import views as home_views
from band import views as bandViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home_views.homepage, name="home"),
    path("accounts/", include('django.contrib.auth.urls')),
    path('credits/', home_views.credits),
    path('about/', home_views.about,name="about"),
    path('news/', home_views.news, name='news'),
    path("musicians/",bandViews.viewAllBands, name="musician_list"),
    path('musician/<int:id>/', bandViews.viewMusicianDetails, name='musician_detail'),
    path('bands/', bandViews.band_list, name='band_list'),
    path('band/<int:id>/', bandViews.band_detail, name='band_detail'),
    path('venues/', bandViews.venue_list, name='venue_list'),
    path('restricted_page/',bandViews.restricted_page, name='restricted_page'),
    path('musician_restricted/<int:musician_id>/',bandViews.musician_restricted, name="restricted_musician"),
]
