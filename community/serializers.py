from rest_framework import serializers

from authentication.serializers import AuthUserSerializer
from community.models import Board, Post, Comment


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "description",
        ]


class PostSerializer(serializers.ModelSerializer):
    user = AuthUserSerializer(read_only=True)
    board_id = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(), source='board', write_only=True
    )
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ["id", "user", "board_id", "title", "content", "comment_count"]

    def create(self, validated_data):
        user = self.context["request"].user
        post = Post.objects.create(user=user, **validated_data)
        return post


class PostRetrieveSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    user = AuthUserSerializer(read_only=True)
    board = BoardSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "board_id",
            "title",
            "content",
            "comment_count",
            "comments",
        ]

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all().order_by("-id"), many=True).data


class CommentSerializer(serializers.ModelSerializer):
    user = AuthUserSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), source='post', write_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "post_id",
            "user",
            "content",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        comment = Comment.objects.create(user=user, **validated_data)
        return comment
