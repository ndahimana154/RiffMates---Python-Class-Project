from django.urls import path
from band import views as bandViews

urlpatterns = [
    path('', bandViews.band_list, name='band_list'),
    path('band/<int:id>/', bandViews.band_detail, name='band_detail'),
    path('musicians/', bandViews.viewAllBands, name='musician_list'),
    path('musician/<int:id>/', bandViews.viewMusicianDetails, name='musician_detail'),
    path('venues/', bandViews.venue_list, name='venue_list'),
    path('venues_list2/', bandViews.venues, name='venue_list2'),
    path('edit_venue2/<int:venue_id>/', bandViews.edit_venue, name="edit_venue2"),
    path('restricted_page/', bandViews.restricted_page, name='restricted_page'),
    path('musician_restricted/<int:musician_id>/', bandViews.musician_restricted, name='restricted_musician'),
]
