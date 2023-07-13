from django.urls import path
from .views import *
from . import views

from django.conf import settings
from django.conf.urls.static import static 

app_name = 'playlist'

urlpatterns = [
    path('albums', views.album_list_create),
    path('albums/<int:album_id>', views.album_detail_update_delete),
    path('albums/<int:album_id>/tracks', views.track_list_create),
    path('albums/<int:album_id>/tracks/<int:track_id>', views.track_detail_update_delete),
    path('tags/<str:tag_name>', views.find_tag)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)