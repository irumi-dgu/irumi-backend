from django.urls import path, include
from rest_framework import routers
from .views import *

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("lanterns", LanternViewSet, basename="lanterns")
report_router = routers.SimpleRouter(trailing_slash=False)
report_router.register("report", ReportViewSet, basename="report")

urlpatterns = [
    path('', include(default_router.urls)),
    path('lanterns/<int:id>/', include(report_router.urls)),
]