"""
URL configuration for irumi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('lantern.urls')),
]
# 만약 DEBUG 모드인 경우 (개발 환경에서)
if settings.DEBUG:
    # 미디어 파일을 서빙하기 위한 URL 패턴을 추가
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# HTTPS로 전환하는 경우, 미디어 파일과 정적 파일을 서빙할 때도 HTTPS를 사용하려면 다음과 같이 설정해야 합니다.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, secure=True)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, secure=True)