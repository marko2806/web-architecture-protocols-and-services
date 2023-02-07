from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Board game API",
      default_version='v1',
      description="Board game API contains records of famous board games and their publishers. Each can be accessed through appropriate URLs",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('board_game_module.urls')),
    re_path(r'', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
