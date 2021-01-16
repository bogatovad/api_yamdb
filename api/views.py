from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, pagination, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import IsAuthorOrReadOnly, IsStaffOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCUDSerializer,
    TitleSerializer,
)


class ReviewModelViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 20
    permission_classes = [IsAuthorOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title_id=title)


class CommentModelViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 20
    permission_classes = [IsAuthorOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_review(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.get_title(),
        )
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review_id=self.get_review())


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 20
    permission_classes = [IsStaffOrReadOnly]


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 20
    permission_classes = [IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_class = TitleFilter
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 20

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return TitleCUDSerializer
        return super().get_serializer_class()
