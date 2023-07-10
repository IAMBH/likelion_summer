from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Track, Album, Tag
from .serializers import AlbumSerializer, TrackSerializer, TagSerializer

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
            
            content = request.data['description']
            print(content)
            tag_list = []
            words = content.split()
            for w in words:
                if w[0] == '#':
                    tag_list.append(w[1:])
            for t in tag_list:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                album = get_object_or_404(Album, id=serializer.data['id'])
                album.tag.add(tag)
            album.save()
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

            album = get_object_or_404(Album, id=serializer.data['id'])
            album.tag.clear()   # 초기화 후 tag 추가 진행
            content = request.data['description']
            tag_list = []
            words = content.split()
            for w in words:
                if w[0] == '#':
                    tag_list.append(w[1:])
            for t in tag_list:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()

                album.tag.add(tag)
            album.save()

        return Response(AlbumSerializer(album).data)

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

@api_view(['GET', 'POST'])
def find_tag(request, tag_name):
    # get_object_or_404 - 하나 찾을때, filter - 여러개 찾을 때?
    finding_tag = get_object_or_404(Tag, name=tag_name)  
    if request.method == 'GET':
        album = Album.objects.filter(tag__in = [finding_tag])
        serializer = AlbumSerializer(album, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        finding_tag = get_object_or_404(Tag, name=request.data['name'])
        album = Album.objects.filter(tag__in = [finding_tag])
        serializer = AlbumSerializer(album, many=True)
        return Response(serializer.data)