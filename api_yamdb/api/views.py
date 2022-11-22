from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail.message import EmailMessage
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Categories, Genres, Review, Title
from users.models import User
from api.filters import TitlesFilter
from api.permissions import (AdminAuthorModeratorOrReadOnly,
                             AdminOrReadOnlySafeMethods, CreaterOrAdmin,
                             IsAuthenticatedAdmin, ReadOnlySafeMethods)
from api.serializers import (CategoriesSerializer, CommentSerializer,
                             GenresSerializer, ReviewSerializer,
                             RoleReadSerializer, SignupSerializer,
                             TitlesRatingSerializer, TitlesSerializer,
                             TokenSerializer, UserSerializer)


@permission_classes((AllowAny,))
@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save
    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")
    try:
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = PasswordResetTokenGenerator().make_token(user)
    except IntegrityError:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    register_email = EmailMessage(
        subject='Welcome on yamdb',
        body=f'ваш код подтверждения: {confirmation_code}',
        from_email='yamdb@yamdb.fake',
        to=(serializer.validated_data['email'],)
    )
    register_email.send()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def obtain_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user_data = get_object_or_404(User, username=username)
    if PasswordResetTokenGenerator().check_token(user_data, confirmation_code):
        token = AccessToken.for_user(user_data)
        return Response({'token': str(token)}, status=status.HTTP_201_CREATED)
    data = {
        'confirmation_code': 'Неверный код',
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (CreaterOrAdmin,)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'], detail=False, url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = RoleReadSerializer(
                request.user, data=request.data, partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnlySafeMethods,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = "slug"


class GenresViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAuthenticatedAdmin | ReadOnlySafeMethods,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = "slug"


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    permission_classes = (IsAuthenticatedAdmin | ReadOnlySafeMethods,)
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    http_method_names = ('get', 'head', 'options', 'post', 'patch', 'delete',)

    def get_serializer_class(self):
        if not self.request.method == 'GET':
            return TitlesSerializer
        return TitlesRatingSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review"""
    serializer_class = ReviewSerializer
    permission_classes = (AdminAuthorModeratorOrReadOnly,)

    def get_queryset(self):
        """Получаем id произведения из эндпоинта"""
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Переопределение создания отзыва"""
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment"""
    serializer_class = CommentSerializer
    permission_classes = (AdminAuthorModeratorOrReadOnly,)

    def get_queryset(self):
        """Получаем id отзыва из эндпоинта"""
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        """Переопределение создания комментария"""
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        )
