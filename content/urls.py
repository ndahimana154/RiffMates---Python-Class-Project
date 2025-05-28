from django.urls import path
from content import views

urlpatterns = [
    path('comment/', views.comment, name='comment'),
    path('comment_accepted/', views.comment_accepted, name='comment_accepted'),
path('list_ads/', views.list_ads, name='list_ads'),
]