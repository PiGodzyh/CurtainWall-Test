"""
URL configuration for AccountManagement project.

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
from django.urls import path
from django.urls import include, path, re_path
# from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import *
from Account.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="幕墙系统API文档",
        default_version='v1',
        description="Welcome to Tongjitumu",
        # terms_of_service="https://www.tweet.org",
        # contact=openapi.Contact(email="demo@tweet.org"),
        # license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("account/", include("Account.urls")),

    # 接口文档
    # 对测试人员更友好
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # 对开发人员更友好
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
