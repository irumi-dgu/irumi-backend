from rest_framework import serializers
from rest_framework.serializers import ListField

from django.contrib.auth.hashers import make_password

from .models import Lantern


class LanternSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField()
    like_cnt = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        lantern = Lantern.objects.create(**validated_data)
        return lantern

    class Meta:
        model = Lantern
        fields = [
            'id',
            'nickname',
            'content',
            'created_at',
            'like_cnt',
            'password'
        ]
        read_only_fields = ['id', 'created_at', 'like_cnt']
        extra_kwargs = {
            'password': {'write_only': True}
        }
