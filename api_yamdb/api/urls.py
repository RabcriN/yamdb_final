from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIGetToken, APISignup, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet)

router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet)
router.register("categories", CategoryViewSet)
router.register("users", UserViewSet, basename="users")
router.register(
    r"titles/(?P<title_id>[^/.]+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments",
    CommentViewSet,
    basename="comments",
)

auth_urls = [
    path('auth/token/', APIGetToken.as_view(), name="token"),
    path('auth/signup/', APISignup.as_view(), name="signup")
]
urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include(auth_urls)),
]
