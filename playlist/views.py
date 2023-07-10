from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Track, Album
from .serializers import AlbumSerializer, TrackSerializer

from django.shortcuts import get_object_or_404
from django.shortcuts import render

@api_view(['GET','POST'])
def album_list_create(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(data = serializer.data)
    elif request.method == 'POST':
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):   # 데이터가 유효한지 검사 : 유호한지의 기준이 db에 데이터가 이미 있을때, 모든 필드가 입력되지 않았을 때 중?
            serializer.save()
            return Response(data=serializer.data)

@api_view(['GET','PATCH','DELETE'])
def album_detail_update_delete(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    
    if request.method=='GET':
        serializer = AlbumSerializer(album)
        return Response(data = serializer.data)
    
    elif request.method == 'PATCH':
        serializer = AlbumSerializer(instance=album, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        album.delete()
        data = {
            'deleted_album': album_id
        }
        return Response(data)
    
@api_view(['GET', 'POST'])
def track_list_create(request, album_id):
    album = get_object_or_404(Album, id=album_id)

    if request.method=='GET':   # model -> JSON
        tracks = Track.objects.filter(album=album)
        serializer = TrackSerializer(tracks, many=True)
        return Response(data=serializer.data)
    
    elif request.method=='POST':    # JSON -> model
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(album=album)
        return Response(serializer.data)
    
@api_view(['GET','PATCH','DELETE'])
def track_detail_update_delete(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    # track = Track.objects.filter(album=album, id=track_id)
    if request.method == 'GET':
        # Sericalizer는 many=True가 아니면(기본값이면) instance를 기대하고 many=True면 queryset을 기대한다.
        # filter를 그대로 즉, TrackSerializer(track)이면 instance 
        # serializer = TrackSerializer(track.first())
        serializer = TrackSerializer(track)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = TrackSerializer(instance=track, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        track.delete()
        data = {
            'deleted_track' : track_id
        }
        return Response(data)
