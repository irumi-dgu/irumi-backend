from django.urls import path, include
from rest_framework import routers
from .views import LanternViewSet

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("lanterns", LanternViewSet, basename="lanterns")

urlpatterns = [
    path('', include(default_router.urls)),
]