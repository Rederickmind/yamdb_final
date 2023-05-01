"""
Вьюшки приложения api.

send_confirmation_code -- Отправка кода подтверждения пользователю.
SignUpView      -- Вьюсет для регистрации пользователя.
TokenObtainView -- Вьюсет для получения токена по коду подтверждения.
UserViewSet     -- Вьюсет для управления пользователями приложения.
                -- Получение и изменение данных пользователя и его удаление.
TitleViewSet    -- Вьюсет для модели Title.
CategoryViewSet -- Вьюсет для модели Category.
GenreViewSet    -- Вьюсет для модели Genre.
ReviewViewSet   -- Вьюсет для модели Review.
CommentViewSet  -- Вьюсет для модели Comment.

"""

from api.permissions import IsAdmin
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Categories, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly,
                          IsAuthorOrIsModeratorOrAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleSerializer, TitleWriteSerializer,
                          TokenSerializer, UserMeSerializer, UserSerializer)


def send_confirmation_code(user):
    """Функция отправки кода подтверждения на почту."""
    confirmation_code = default_token_generator.make_token(user)
    return send_mail(
        subject=settings.EMAIL_SUBJECT,
        message=f'Код подтверждения: {confirmation_code}',
        from_email=settings.EMAIL_ADMIN,
        recipient_list=[user.email]
    )


class SignUpView(generics.CreateAPIView):
    """Регистрация нового пользователя по username и email."""

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """Обработка POST запроса с данными пользователя."""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(generics.CreateAPIView):
    """Получение токена по имени пользователя и коду подтверждения из почты."""

    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """Обработка данных пользователя перед выдачей токена."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status.HTTP_200_OK)
        return Response(
            {'message': 'Неверный код подтверждения.'},
            status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    Управление пользователями.

    Создание пользователя от администратора.
    Получение и изменение данных пользователя.
    Удаление пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request):
        """
        Функция для эндпоинта /users/me/.

        -- Получение данных своей учетной записи.
        -- Изменение данных своей учетной записи.

        """
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                self.request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(self.request.user)
        return Response(serializer.data)


class TitleViewSet(ModelViewSet):
    """
    Вьюсет для модели Title.

    get_serializer_class -- Возвращает сериализатор
                            в зависимости от метода.
    """

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()

    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от метода."""
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleWriteSerializer


class GenreReviewViewSet(ModelViewSet):
    """
    Базовый класс для моделей Category и Genre.

    retrieve -- Возвращает ответ со статусом 405 по методу GET.
    update   -- Возвращает ответ со статусом 405 по методу PUT.
    """

    permission_classes = [IsAdminOrReadOnly]
    spagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        """Возвращает ответ со статусом 405 по методу GET."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        """Возвращает ответ со статусом 405 по методу PUT."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(GenreReviewViewSet):
    """Вьюсет для модели Category."""

    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenreReviewViewSet):
    """
    Вьюсет для модели Genre.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(ModelViewSet):
    """
    Вьюсет для модели Review.

    get_queryset   -- Возвращает queryset отзывов по id произведения.
    perform_create -- Осуществляет создание нового отзыва.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrIsModeratorOrAdminOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        """Возвращает queryset отзывов по id произведения."""
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """
        Осуществляет создание нового отзыва.

        Добавляет пользователя, отправившего запрос,
        в поле автора отзыва.
        """
        title_id = self.kwargs['title_id']
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=title_id)
        )


class CommentViewSet(ModelViewSet):
    """
    Вьюсет для модели Comment.

    get_queryset   -- Возвращает queryset комментариев по отзыву.
    perform_create -- Осуществляет создание нового комментария.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrIsModeratorOrAdminOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        """Возвращает queryset комментариев по отзыву."""
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """
        Осуществляет создание нового комментария.

        Добавляет пользователя, отправившего запрос,
        в поле автора комментария.
        """
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
