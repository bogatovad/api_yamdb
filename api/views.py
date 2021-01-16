from rest_framework import pagination
from rest_framework.response import Response

from .paginator import CustomPagination
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated

from .models import (
    Review,
    Title,
    Category,
    Genre
                     )
from .permission import AdminForCreator
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    TitleSerializer,
    GenreSerializer
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
        queryset = self.get_queryset()
        if queryset.filter(author=self.request.user, title_id=self.get_title()).exists():
            raise ValidationError({'non_field_errors': ['cannot add another review']})
        serializer.save(author=self.request.user, title_id=self.get_title())


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
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 20
    permission_classes = [IsAuthenticatedOrReadOnly, AdminForCreator]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.delete()
        # queryset = get_object_or_404(Category, slug=instance)



    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
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
