from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentModelViewSet,
    GenreViewSet,
    ReviewModelViewSet,
    TitleViewSet,
)

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, 'title')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewModelViewSet,
    'review',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentModelViewSet,
    'comment',
)
v1_router.register(
    'categories',
    CategoryViewSet,
    'categorys',
)
v1_router.register(
    'genres',
    GenreViewSet,
    'genres'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
