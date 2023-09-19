from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LanternViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'lanterns', LanternViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
