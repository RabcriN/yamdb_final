from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import IsAdminOnly, IsAdminOrReadOnly, IsAuthorModeratorAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer)


class MixinViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TitleWriteSerializer
        return TitleReadSerializer


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    pagination_class = PageNumberPagination


class CategoryViewSet(MixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    http_method_names = (
        "get",
        "post",
        "delete",
    )
    lookup_field = "slug"
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdmin,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        author = self.request.user
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdmin,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


def send_confirmation_code(user):
    """Отправка кода на почту"""
    confirmation_code = default_token_generator.make_token(user)
    subject = "Код подтверждения на сервисе YaMDb"
    message = f"{confirmation_code} - ваш код авторизации на сервисе YaMDb"
    admin_email = settings.DEFAULT_FROM_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsAdminOnly,
    )
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        detail=False,
        methods=("GET", "PATCH"),
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Профайл пользователя."""
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """Создание и отправка."""
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGetToken(TokenViewBase):
    """Получение JWT-токена."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.data["username"]
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data["confirmation_code"]
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
