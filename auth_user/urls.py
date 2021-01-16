from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

v1_router = DefaultRouter()
v1_router.register('users', views.UserViewSet, basename='users')


urlpatterns = [
    path('v1/api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
    path("v1/token/", csrf_exempt(views.get_token), name="token_obtain_pair"),
    path('v1/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/auth/email/', csrf_exempt(views.email)),
    path('v1/users/me/', views.get_info_me),
    path('v1/', include(v1_router.urls)),
]
