from django.db import models

from common.models import BaseModel


class Board(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "board"
        indexes = [models.Index(fields=["title"])]


class Post(BaseModel):
    board = models.ForeignKey(
        "community.Board", on_delete=models.CASCADE, related_name="posts"
    )
    user = models.ForeignKey(
        "authentication.AuthUser", on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    comment_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "post"
        indexes = [
            models.Index(fields=["board", "user"]),
            models.Index(fields=["comment_count"]),
        ]


class Comment(BaseModel):
    post = models.ForeignKey(
        "community.Post", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        "authentication.AuthUser", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()

    class Meta:
        db_table = "comment"
        indexes = [models.Index(fields=["post", "user"])]
