from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from uuid import uuid4

from .models import *
from .serializers import LanternSerializer

from django.db.models import Count, Q

class LanternViewSet(viewsets.ModelViewSet):
    queryset = Lantern.objects.annotate(
        like_cnt=Count(
            "reactions", filter=Q(reactions__reaction="like"), distinct=True
        )
    ).order_by('-created_at') 

    serializer_class = LanternSerializer

    @action(methods=["POST"], detail=True, permission_classes=[AllowAny])
    def likes(self, request, pk=None):
        lantern = self.get_object()

        # 쿠키에서 user_id 가져오기. 없으면 새로 생성.
        user_id = request.COOKIES.get('user_id', str(uuid4()))

        # 이미 'like' reaction이 있는지 확인
        existing_like = LanternReaction.objects.filter(lantern=lantern, user_id=user_id, reaction="like").first()

        # 이미 'like'가 있다면 삭제
        if existing_like:
            existing_like.delete()
            response_data = {"status": "좋아요 취소"}
        else:
            # 'like'가 없다면 추가
            LanternReaction.objects.create(lantern=lantern, user_id=user_id, reaction="like")
            response_data = {"status": "좋아요"}

        # Response 객체 생성
        response = Response(response_data)

        # 쿠키 설정
        response.set_cookie('user_id', user_id, max_age=365*24*60*60)  # 유효기간 1년

        return response
