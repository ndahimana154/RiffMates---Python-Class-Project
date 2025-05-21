from django.urls import path
from band import views as bandViews

urlpatterns = [
    path('', bandViews.band_list, name='band_list'),
    path('band/<int:id>/', bandViews.band_detail, name='band_detail'),
    path('musicians/', bandViews.viewAllBands, name='musician_list'),
    path('musician/<int:id>/', bandViews.viewMusicianDetails, name='musician_detail'),
    path('venues/', bandViews.venue_list, name='venue_list'),
    path('restricted_page/', bandViews.restricted_page, name='restricted_page'),
    path('musician_restricted/<int:musician_id>/', bandViews.musician_restricted, name='restricted_musician'),
]
