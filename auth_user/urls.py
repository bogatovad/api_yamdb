from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

v1_router = DefaultRouter()
v1_router.register('users', views.UserViewSet, basename='users')

auth_paths = [
    path("token/", csrf_exempt(views.get_token), name="token_obtain_pair"),
    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('email/', csrf_exempt(views.email)),
]

urlpatterns = [
    path('v1/auth/', include(auth_paths)),
    path('v1/', include(v1_router.urls)),
]
