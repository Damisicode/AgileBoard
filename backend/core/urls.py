from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from boards.api.urls import board_router

router = DefaultRouter()
router.registry.extend(board_router.registry)

API_TITLE = 'AgileBoard Backend API'
API_DESCRIPTION = 'A Web API for a kanban style project management tool.'
schema_view = get_swagger_view(title=API_TITLE)

urlpatterns = [
    # Admin path
    path('admin/', admin.site.urls),

    # Authentication path
    re_path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/registration/', include('rest_auth.registration.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/', include(router.urls)),

    # Board paths
    path('api/v1/board/', include('boards.api.urls')),

    # documentation
    path('docs/', include_docs_urls(title=API_TITLE,
                                    description=API_DESCRIPTION)),

    # swagger docs path
    path('swagger-docs/', schema_view),
]