from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse

from rest_framework_simplejwt.serializers import User
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from .serializer import UserSerializer, UserMeSerializers
from .models import User
from .permissions import IsAdministrator


@api_view(['POST'])
def email(requests):
    """Send confirmation_code by email."""
    email = requests.POST['email']
    user = User.objects.get_or_create(username=email, email=email, is_active=False)[0]
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
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return JsonResponse({'token': str(token)})
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username',]
    lookup_field = 'username'
    permission_classes = [IsAdministrator,]

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = User.objects.filter(username=request.user)[0]
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserMeSerializers(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)