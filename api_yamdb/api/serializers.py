"""
Сериализаторы приложения api.

GenreSerializer    -- Сериализатор модели Genre.
CategorySerializer -- Сериализатор модели Category.
TitleSerializer    -- Сериализатор модели Title.
ReviewSerializer   -- Сериализатор модели Review.
CommentSerializer  -- Сериализатор модели Comment.
SignUpSerializer   -- Сериализатор для вьюсета регистрации пользователя.
TokenSerializer    -- Сериализатор для вьюсета получения токена пользователем.
UserSerializer     -- Сериализатор для модели User.
UserMeSerializer   -- Сериализатор для работы с данными своей учетной записи

"""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Categories, Comment, Genre, Review, Title
from reviews.validators import validate_one_to_ten
from users.models import User
from users.validators import validate_email_address, validate_username


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Genre.

    Субклассы:
    Meta -- Метакласс сериализатора GenreSerializer.
    """

    class Meta:
        """Метакласс сериализатора GenreSerializer."""

        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Category.

    Субклассы:
    Meta -- Метакласс сериализатора CategorySerializer.
    """

    class Meta:
        """Метакласс сериализатора CategorySerializer."""

        model = Categories
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Title.

    get_rating -- Возвращает округлённую среднюю оценку
                  всех произведений.

    Субклассы:
    Meta -- Метакласс сериализатора TitleSerializer.
    """

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """Метакласс сериализатора TitleSerializer."""

        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор записи для модели Title.

    Субклассы:
    Meta -- Метакласс сериализатора TitleWriteSerializer.
    """

    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        """Метакласс сериализатора TitleWriteSerializer."""

        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Review.

    validate_score -- Проверяет правильность поля score.
    validate       -- Проверяет уникальность пары "произведение, автор".

    Субклассы:
    Meta -- Метакласс сериализатора ReviewSerializer.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Метакласс сериализатора ReviewSerializer."""

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'pub_date')

    def validate_score(self, value):
        """Проверяет правильность поля score."""
        validate_one_to_ten(value, serializers.ValidationError)
        return value

    def validate(self, data):
        """Проверяет уникальность пары "произведение, автор"."""
        request = self.context['request']
        title_id = request.parser_context['kwargs']['title_id']
        author = request.user
        same_review = Review.objects.filter(author=author, title=title_id)
        if same_review.exists() and request.method == 'POST':
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение'
            )
        return data


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для вьюсета регистрации пользователя."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[validate_email_address]
    )

    def validate(self, data):
        """
        Валидация данных при регистрации пользователя.

        -- Проверка существования пары пользователь/e-mail
        для повторной отправки кода подтверждения.
        -- Проверка для запрета регистрации нового пользователя
        с уже зарегистрированным в приложении username.
        -- Проверка для запрета регистрации нового пользователя
        с уже зарегистрированным в приложении e-mail.
        """
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует!'
            )
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для вьюсета получения токена."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью User."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        """Метакласс сериализатора для модели User."""

        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для данных о своей учётной записи."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        """Метакласс сериализатора данных своей учетной записи."""

        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Comment.

    Субклассы:
    Meta -- Метакласс сериализатора CommentSerializer.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Метакласс сериализатора CommentSerializer."""

        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date')
