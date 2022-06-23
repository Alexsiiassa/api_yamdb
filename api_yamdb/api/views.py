from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import (Category, Genre, Review,
                            Title, User, UserRole)

from .filters import TitleFilter
from .mixins import CreateListDestroyMixinSet
from .permissions import IsAdmin, IsAdminModerator, IsAnon
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetCodeSerializer,
                          GetTokenSerializer, ReviewSerializer,
                          TitleCUDSerializer, TitleSerializer,
                          UserSerializer)


class CategoryViewSet(CreateListDestroyMixinSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyMixinSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAnon | IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all().order_by('-id')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCUDSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModerator]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModerator]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review.comments.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    pagination_class = PageNumberPagination
    permission_classes = [IsAdmin]
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            user = self.request.user
            serializer = UserSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)

        if request.method == 'PATCH':
            user = get_object_or_404(User, id=request.user.id)
            fixed_data = self.request.data.copy()
            if ('role' in self.request.data
                    and user.role == UserRole.USER.value):
                fixed_data['role'] = UserRole.USER.value
            serializer = UserSerializer(
                user,
                data=fixed_data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            data=request.data,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    """Получить код подтверждения на указанный email"""
    serializer = GetCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    try:
        user, exist = User.objects.get_or_create(
            username=username,
            email=email,
            is_active=False
        )
    except Exception:
        return Response(request.data,
                        status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    User.objects.filter(username=username).update(
        confirmation_code=confirmation_code
    )
    subject = 'Регистрация на YAMDB'
    message = f'Код подтверждения: {confirmation_code}'
    send_mail(subject, message, 'YAMDB', [email])
    return Response(
        request.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получить токен для работы с API по коду подтверждения"""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)
