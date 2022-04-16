from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIgetToken, APIsignup, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet)


router_v1 = DefaultRouter()

app_name = 'api'

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
auth = [
    path('token/', APIgetToken.as_view(), name='token'),
    path('signup/', APIsignup.as_view(), name='signup'),
]
urlpatterns = [
    path('v1/auth/', include(auth)),
    path('v1/', include(router_v1.urls)),
]
