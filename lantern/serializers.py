from rest_framework import serializers
from rest_framework.serializers import ListField

from .models import Lantern


class LanternSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField()
    like_cnt = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def create(self, validated_data):
        lantern = Lantern.objects.create(**validated_data)
        return lantern

    class Meta:
        model = Lantern
        fields = [
            'id',
            'nickname',
            'content',
            'created_at',
            'like_cnt'
        ]
        read_only_fields = ['id', 'created_at', 'like_cnt']
