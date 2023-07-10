from rest_framework import serializers
from .models import Track, Album, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    tracks = serializers.SerializerMethodField(read_only=True)
    def get_tracks(self, instance):
        track_list = []
        serializer = TrackSerializer(instance.tracks, many=True)
        for d in serializer.data:
            track_list.append(d['title'])
        return track_list
    
    tag = serializers.SerializerMethodField(read_only=True)
    def get_tag(self, instance):
        tag_list = []
        tags = instance.tag.all()
        for t in tags:
            tag_list.append(t.name)
        return tag_list
    
    class Meta:
        model = Album
        fields = '__all__'
        fields = ['id','artist','title','released','description','tracks','tag']
        # read_only_fields = ['id']

class TrackSerializer(serializers.ModelSerializer):
    # 다르게 보여주고 싶은 field를 SerializerMethodField로 선언
    album = serializers.SerializerMethodField()

    def get_album(self, instacne):  # get_[field] 선언을 통해 원하는 값을 return
        return instacne.album.title

    class Meta:
        model = Track
        fields = ['title', 'track_number', 'album']
        read_only_fields = ['id', 'album']  # read_only_fields에 넣어서 post에 포함이 되지 않아도 되게 함, 읽기전용

