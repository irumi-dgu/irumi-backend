from django.urls import path, include
from rest_framework import routers
from .views import *

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("lamplights", LampViewSet, basename="lamplights")

urlpatterns = [
    path('', include(default_router.urls)),
]