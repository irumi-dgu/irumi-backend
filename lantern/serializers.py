from rest_framework import serializers
from rest_framework.serializers import ListField

from django.contrib.auth.hashers import make_password

from .models import *

# 랜턴 리스트만 보여주는 시리얼라이저
class LanternListSerializer(serializers.ModelSerializer):
    like_cnt = serializers.SerializerMethodField()
    light_bool = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_light_bool(self, instance):
        like_count = self.get_like_cnt(instance)
        if instance.like_cnt >= 10:
            return True
        return False
    
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
            'password',
            'like_cnt', 
            'light_bool',
            'lanternColor',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class LanternDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField()
    like_cnt = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_reported = serializers.SerializerMethodField()
    light_bool = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_is_liked(self, obj):
        user_id = self.context.get('user_id')
        if not user_id:
            return False
        return LanternReaction.objects.filter(lantern=obj, user_id=user_id, reaction="like").exists()

    def get_is_reported(self, obj):
        user_id = self.context.get('user_id')
        if not user_id:
            return False
        return Report.objects.filter(lantern=obj, user_id=user_id).exists()

    def get_light_bool(self, instance):
        like_count = self.get_like_cnt(instance)
        if instance.like_cnt>= 10:
            return True
        return False
        

    class Meta:
        model = Lantern
        fields = [
            'id',
            'nickname',
            'content',
            'created_at',
            'like_cnt',
            'password',
            'light_bool',
            'is_liked',
            'is_reported',
            'lanternColor',
        ]
        read_only_fields = ['id', 'created_at', 'like_cnt', 'light_bool', 'is_liked', 'is_reported']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ReportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCategory
        fields = ('name',)

class ReportSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField()
    lantern = serializers.IntegerField(source='lantern.id')
    user_id = serializers.CharField()

    class Meta:
        model = Report
        fields = ('id', 'created_at', 'lantern', 'user_id')
