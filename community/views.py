from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsOwnerOrReadOnly
from community.models import Board, Comment, Post
from community.serializers import (BoardSerializer, CommentSerializer,
                                   PostRetrieveSerializer, PostSerializer)


class BoardViewSet(viewsets.GenericViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_backends = [filters.OrderingFilter]
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    order_fields = ["id"]
    ordering = ["-id"]


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.select_related("user", "board").prefetch_related("comments").all()
    )
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["board", "user"]
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination
    order_fields = ["id"]
    ordering = ["-id"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostRetrieveSerializer
        return PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("user", "post").all()
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["post", "user"]
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination
    order_fields = ["id"]
    ordering = ["-id"]

    def perform_create(self, serializer):
        post = serializer.validated_data["post"]
        post.comment_count += 1
        post.save()
        serializer.save()

    def perform_destroy(self, instance):
        post = instance.post
        post.comment_count = max(0, post.comment_count - 1)  # 음수 방지 처리
        post.save()
        instance.delete()
