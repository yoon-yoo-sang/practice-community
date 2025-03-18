from rest_framework.routers import DefaultRouter

from community.views import BoardViewSet, CommentViewSet, PostViewSet

app_name = "community"

router = DefaultRouter()

router.register(r"boards", BoardViewSet, basename="board")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls
