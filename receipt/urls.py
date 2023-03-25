"""receipt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularJSONAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views

urlpatterns = [
    path(f'api/v1/{settings.ADMIN_URL}', admin.site.urls),
    path('api/v1/token-auth/', views.obtain_auth_token),
    path('api/v1/culinary/', include('culinary.api.v1.urls')),
    path('api/v1/directory/', include('directory.api.v1.urls')),
    path('api/v1/telegram_bot/', include('telegram_bot.api.v1.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.SWAGGER_URL:
    urlpatterns += [
        path('api/v1/Go9lYiNcza68F2lzPrX/', SpectacularAPIView.as_view(urlconf=urlpatterns), name='schema'),
        path('api/v1/Go9lYiNcza68F2lzPrX.json', SpectacularJSONAPIView.as_view(urlconf=urlpatterns), name='schema'),
        path(f'api/v1/{settings.SWAGGER_URL}', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
