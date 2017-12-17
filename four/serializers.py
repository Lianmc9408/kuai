from four import models
from rest_framework import serializers

class ArticalSerialzer(serializers.ModelSerializer):
    # 外键的情况
    cover_url = serializers.CharField(source='cover_url.images_url')
    class Meta:
        model = models.Artical
        # fields = "__all__"
        fields = ("a_id", "title", "artical", "cover_url")

    # def create(self, validated_data):
    #     return models.Artical.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.cover_url = validated_data.get('cover_url', instance.cover_url)
    #     instance.save()
    #     return instance

class ImagesUrlSerialzer(serializers.ModelSerializer):
    # images_urls = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='images_urls-detail')

    class Meta:
        model = models.ImagesUrl
        # fields = ('images_url', 'images_urls')
        fields = "__all__"
