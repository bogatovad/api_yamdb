from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import User
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
import csv

from django.http import JsonResponse
from rest_framework import pagination, mixins, filters
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated

from .models import (
    Review,
    Title,
    Category,
    Genre,
    User
                     )
from .permission import AdminForCreator, IsAdministrator
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    TitleSerializer,
    GenreSerializer,
    UserSerializer
                          )

@api_view(['POST'])
def email(requests):
    """Send confirmation_code by email."""
    email = requests.POST['email']
    user = User.objects.get_or_create(username=email, email=email)[0]
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Подтверждение регистрации',
              f'Пожалуйста, сохраните этот код : {confirmation_code},'
              ' он Вам понадобиться для получения токена',
              'prakticum@yandex.ru',
              [email], fail_silently=False)
    return JsonResponse({'email': email})


@api_view(['POST'])
def get_token(request):
    """Generate access token."""
    email = request.POST['email']
    confirmation_code = request.POST['confirmation_code']
    user = User.objects.filter(email=email)[0]
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return JsonResponse({'token': str(token)})
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]
    lookup_field = 'username'
    permission_classes = [IsAdministrator, ]


@permission_classes(IsAuthenticated,)
@api_view(['GET', 'PATCH'])
def get_info_me(request):
    if not request.user.is_anonymous:
        user = User.objects.filter(username=request.user)[0]
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user,
                                        data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)



class ReviewModelViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 20
    # permission_classes = [...]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title_id=self.get_title())


class CommentModelViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 20
    # permission_classes = [...]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.get_title(),
        )

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
    permission_classes = [AdminForCreator]


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    permission_classes = [AdminForCreator]


# class TitleViewSet(viewsets.ModelViewSet):
#     queryset = Title.objects.all()
#     serializer_class = TitleSerializer
#     permission_classes = [IsAuthenticated,
#                           IsAuthenticatedOrReadOnly,]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['year', ]


def fill_base(file_object, object):
    """
    Read a CSV file using csv.DictReader
    """

    reader = csv.DictReader(file_object, delimiter=',')
    for line in reader:
        if object == 'category':
            Category.objects.create(id=line['id'], name=line['name'],
                                    slug=line['slug'])
        if object == 'titles':
            category = Category.objects.get(id=int(line['category']))
            Title.objects.create(name=line['name'], year=line['year'],
                                 category=category)
        if object == 'genre':
            Genre.objects.create(id=line['id'], name=line['name'],
                                 slug=line['slug'])


def fill(request, object):
    path = f'data/{object}.csv'

    with open(path, "r") as file_object:
        fill_base(file_object, object)

    return JsonResponse({object: 'fill'})




