import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .pagination import CommentsPagination, ReviewsPagination, TitlesPagination
from .permissions import (IsAdmin, IsAdminOrReadOnly, ReadOnlyPermission,
                          ReviewCommentPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUsersSerializer, GenreSerializer,
                          ReviewCreateSerializer, ReviewSerializer,
                          SignupSerializer, TitleReadSerializer,
                          TitleSerializer, TitleWriteSerializer,
                          TokenSerializer)

User = get_user_model()


class APIsignup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data.get('email')
        confirmation_code = random.randint(100000, 999999)
        send_mail('Confirmation code',
                  f'Your code for getting a token - {confirmation_code}.',
                  settings.DEFAULT_EMAIL,
                  [email, ],
                  fail_silently=False,)
        serializer.save(confirmation_code=confirmation_code)
        return Response(serializer.validated_data, status=HTTP_200_OK)


class APIgetToken(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data.get('email')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(
            User, email=email, confirmation_code=confirmation_code)
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)},
                        status=HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUsersSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['GET', 'PATCH'], url_path='me')
    def get_or_patch_me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        serializer = self.get_serializer(
            instance=request.user,
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score')
                                            ).order_by('-name')
    serializer_class = TitleSerializer
    permission_classes = (ReadOnlyPermission | IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer


class CreateListDestroyVieSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class GenreViewSet(CreateListDestroyVieSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = TitlesPagination

    def get_object(self):
        return get_object_or_404(Genre, slug=self.kwargs.get('slug'))


class CategoryViewSet(CreateListDestroyVieSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin | ReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = "slug"
    pagination_class = TitlesPagination

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs.get('slug'))


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)
    pagination_class = ReviewsPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)
    pagination_class = CommentsPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
