from rest_framework import viewsets, mixins, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from uuid import uuid4

import pandas as pd
import random
import os

from .models import *
from .serializers import *
from .paginations import LanternPagination
from .filters import LanternFilter

from django.db.models import Count, Q
from django.contrib.auth.hashers import check_password, make_password
from django_filters import rest_framework as filters
from django.contrib.staticfiles import finders
from django.conf import settings
from django.http import BadHeaderError
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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

    serializer_class = LanternListSerializer
    detail_serializer_class = LanternDetailSerializer
    pagination_class = LanternPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LanternFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                print("현재 detail serializer를 사용중")
                return self.detail_serializer_class
        print("현재 list serializer를 사용중")
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.COOKIES.get('user_id', None)
        return context

    def create(self, request, *args, **kwargs):
        # 닉네임에 공백이 포함되어 있는지 검사
        nickname = request.data.get('nickname', '').strip()
        if ' ' in nickname:
            return Response({"detail": "공백없이 닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호를 해시하여 저장
        password = request.data.get('password')
        hashed_password = make_password(password)

        # request.data의 복사본을 생성
        data = request.data.copy()
        data['password'] = hashed_password

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_random_fortune_from_excel(self):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'fortune.xlsx')
        df = pd.read_excel(file_path)
        fortune = random.choice(df['fortune'].tolist())
        return fortune

    @receiver(post_save, sender=LanternReaction)
    def update_likes_count(sender, instance, created, **kwargs):
        if created and instance.reaction == "like":
            total_likes = LanternReaction.objects.filter(lantern=instance.lantern, reaction="like").count()
            if total_likes >= 10:
                instance.lantern.light_bool = True
                instance.lantern.save()

    @receiver(post_delete, sender=LanternReaction)
    def decrement_likes_count(sender, instance, **kwargs):
        if instance.reaction == "like":
            total_likes = LanternReaction.objects.filter(lantern=instance.lantern, reaction="like").count()
            if total_likes < 10:
                instance.lantern.light_bool = False
                instance.lantern.save()

    #좋아요 누를 시 쿠키 기반으로 막기
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

    #글 삭제 시 비밀번호 입력
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

    #최신순 정렬
    @action(detail=False, methods=["GET"])
    def recent(self, request):
        lanterns = self.filter_queryset(self.queryset.order_by("-created_at"))
        page = self.paginate_queryset(lanterns)  
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)  

    #응원순 정렬, 전부 like 0개면 걍 최신순으로 뜨게 함(라이크 수 같아도)
    @action(detail=False, methods=["GET"])
    def pop(self, request):
        lanterns = self.filter_queryset(self.queryset.order_by("-like_cnt"))
        page = self.paginate_queryset(lanterns)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["GET"], permission_classes=[AllowAny])
    def cookie(self, request):
        user_id = request.COOKIES.get('user_id')
        if not user_id:
            user_id = str(uuid4())  # 새로운 user_id 생성
            new_cookie = True
        else:
            new_cookie = False

        fortune = Fortune.objects.filter(user_id=user_id).first()

        # 이미 해당 사용자에게 할당된 fortune이 있다면 반환
        if fortune:
            response = Response({"fortune": fortune.fortune})
        else:
            # 아니라면 새 fortune 할당
            fortune = self.get_random_fortune_from_excel()
            Fortune.objects.create(user_id=user_id, fortune=fortune)
            response = Response({"fortune": fortune})

        if new_cookie:
            response.set_cookie('user_id', user_id, max_age=365*24*60*60)  # 유효기간 1년으로 해뒀는디 바꿔도 됨

        return response

    @action(detail=True, methods=["POST"], url_path='report')
    def report(self, request, pk=None):
        lantern = self.get_object()
        
        existing_cookie_key = request.COOKIES.get(str(lantern.id))
        if existing_cookie_key:
            return Response({'detail': '이미 신고한 게시글입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        report_key = get_random_string(length=10)
        report = Report.objects.create(lantern=lantern, key=report_key)

        serializer = ReportSerializer(report)
        data = serializer.data

        response = Response(data, status=status.HTTP_201_CREATED)
        response.set_cookie(str(lantern.id), report_key, max_age=365*24*60*60)  # 1년 동안 유효

        return response
    
    @action(detail=False, methods=["GET"], url_path='random')
    def rand(self, request):
        queryset = self.get_queryset()
        totCount = queryset.count()
        lanterns = queryset.order_by("?")[:20]
        serializer = self.get_serializer(lanterns, many=True)
        
        return Response({
            'totCount': totCount,
            'lanterns': serializer.data
        })