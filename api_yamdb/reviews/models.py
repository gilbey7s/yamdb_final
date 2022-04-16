from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from .validators import validate_me

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

DICT_ROLE = [
    (USER, "user"),
    (MODERATOR, "moderator"),
    (ADMIN, "admin"),
]


class CustomUser(AbstractUser):

    email = models.EmailField("email address", unique=True, max_length=254,)
    bio = models.TextField("biography", blank=True,)
    role = models.CharField(
        "user role",
        max_length=16,
        choices=DICT_ROLE,
        default=USER,
        blank=True,
    )
    confirmation_code = models.IntegerField("code", default=0,)
    username = models.CharField(
        "username",
        validators=(
            validate_me,
        ),
        unique=True,
        max_length=150,
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ['-username', ]


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='название',
                            unique=True
                            )
    slug = models.SlugField(unique=True, verbose_name='уникальный id')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['-name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='название',
                            unique=True
                            )
    slug = models.SlugField(unique=True, verbose_name='уникальный id')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['-name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='название')
    year = models.PositiveSmallIntegerField(
        verbose_name='год',
        help_text='Введите год в формате: YYYY'
    )
    description = models.TextField(verbose_name='описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name, self.year, self.category


class GenreTitle(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='genres',
                              verbose_name='произведение'
                              )
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              related_name='titles',
                              verbose_name='жанр'
                              )

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'жанры произведений'
        constraints = [
            UniqueConstraint(fields=['title', 'genre'],
                             name='unique_genre_title')
        ]


class Review(models.Model):
    text = models.TextField(verbose_name="Отзыв")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True
    )
    score = models.IntegerField(
        'Оценка', validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Оцените от 1 до 10",)
    title = models.ForeignKey(
        Title, unique=False, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        ordering = ['id']
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review')
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
