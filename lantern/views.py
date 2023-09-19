from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from uuid import uuid4

from .models import *
from .serializers import LanternSerializer

from django.db.models import Count, Q
from django.contrib.auth.hashers import check_password

class LanternViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Lantern.objects.annotate(
        like_cnt=Count(
            "reactions", filter=Q(reactions__reaction="like"), distinct=True
        )
    ).order_by('-created_at') 

    serializer_class = LanternSerializer

    @action(methods=["POST"], detail=True, permission_classes=[AllowAny])
    def likes(self, request, pk=None):
        lantern = self.get_object()

        # 쿠키에서 user_id 가져오기. 없으면 새로 생성!
        user_id = request.COOKIES.get('user_id', str(uuid4()))

        # 이미 좋아요 눌렀는지 확인
        existing_like = LanternReaction.objects.filter(lantern=lantern, user_id=user_id, reaction="like").first()

        # 이미 'like'가 있다면 삭제
        if existing_like:
            existing_like.delete()
            response_data = {"status": "좋아요 취소"}
        else:
            # 'like'가 없다면 추가
            LanternReaction.objects.create(lantern=lantern, user_id=user_id, reaction="like")
            response_data = {"status": "좋아요"}

        response = Response(response_data)

        response.set_cookie('user_id', user_id, max_age=365*24*60*60)  # 유효기간 1년임

        return response

    @action(methods=['POST'], detail=True, permission_classes=[AllowAny])
    def delete(self, request, pk=None):
        lantern = self.get_object()
        
        password_provided = request.data.get('password')

        if not password_provided:
            return Response({'detail': '비밀번호를 입력해주세요.'}, status=400)

        # db 비밀번호랑 일치 여부 확인
        if check_password(password_provided, lantern.password):
            lantern.delete()
            return Response({'detail': '글이 성공적으로 삭제되었습니다.'}, status=204)
        else:
            return Response({'detail': '비밀번호가 틀렸습니다.'}, status=400)
