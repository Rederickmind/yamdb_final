"""URL-ы приложения api."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignUpView, TitleViewSet,
                       TokenObtainView, UserViewSet)

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet)
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(
    prefix=r'titles/(?P<title_id>\d+)/reviews',
    viewset=ReviewViewSet,
    basename='review'
)
router_v1.register(
    prefix=r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    viewset=CommentViewSet,
    basename='comment'
)
router_v1.register(
    prefix=r'users',
    viewset=UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenObtainView.as_view()),
    path('v1/', include(router_v1.urls)),
]
