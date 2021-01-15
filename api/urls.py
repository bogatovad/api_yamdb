from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (
    CommentModelViewSet,
    ReviewModelViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    get_info_me,
    get_token,
    email,

)

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')
router.register(
    'categories',
    CategoryViewSet,
    'categorys',
)
router.register(
    'genres',
    GenreViewSet,
    'genres'
)

urlpatterns = [
    path('v1/users/me/', get_info_me),
    path('v1/', include(router.urls)),
    path('v1/token/', csrf_exempt(get_token), name='token_obtain_pair'),
    path('v1/auth/email/', csrf_exempt(email)),
    path('v1/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]