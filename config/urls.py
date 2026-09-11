"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from apps.note.views import RegisterView
from drf_spectacular.renderers import OpenApiJsonRenderer
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

class SpectacularJSONView(SpectacularAPIView):
    renderer_classes = [OpenApiJsonRenderer]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.note.urls")),
    # آدرس لاگین: نام کاربری و رمز را می‌گیرد و کلید دیجیتال (Token) تحویل می‌دهد
    path("api/login/", obtain_auth_token, name="api_login"),
    # آدرس ثبت‌نام: نام کاربری و رمز جدید را می‌گیرد، کاربر می‌سازد و توکن می‌دهد
    path("api/register/", RegisterView.as_view(), name="api_register"),
    # مسیرهای سواگر و نقشه API
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema.json", SpectacularJSONView.as_view(), name="schema-json"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]


