from django.shortcuts import render
from rest_framework import viewsets, mixins

from .serializers import *
from .models import *

class LampViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin):

    queryset = Lamplight.objects.all()
    serializer_class = LamplightSerializer