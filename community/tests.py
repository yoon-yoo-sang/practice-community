from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import AuthUser
from community.models import Board, Post, Comment


class TestCommunity(TestCase):
    def setUp(self):
        self.board_count = 4
        self.post_count = 4
        self.comment_count = 4

        self.user = AuthUser.objects.create_user(
            username="test",
            email="yysss61888@gmail.com",
            password="password",
        )

        for _ in range(self.board_count):
            board = Board.objects.create(title="title", description="description")

            for _ in range(self.post_count):
                post = Post.objects.create(board=board, user=self.user, title="title", content="content")

                for _ in range(self.comment_count):
                    Comment.objects.create(post=post, user=self.user, content="content")

    def test_board_success(self):
        url = reverse("community:board")
        offset = 1
        limit = 3

        self.authenticate()

        response = self.client.get(url + f"?offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), limit)

        expected_board_count = 1
        offset = self.board_count - expected_board_count
        limit = 3

        response = self.client.get(url + f"?offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_board_count)

    def test_post_success(self):
        url = reverse("community:post")
        board = Board.objects.first()
        offset = 1
        limit = 3

        self.authenticate()

        response = self.client.get(url + f"?board={board.id}&offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), limit)

        expected_post_count = 1
        offset = self.post_count - expected_post_count
        limit = 3

        response = self.client.get(url + f"?board={board.id}&offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_post_count)

        response = self.client.post(url, {"board": board.id, "title": "title", "content": "content"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url + f"?board={board.id}&offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_post_count + 1)

    def test_comment_success(self):
        url = reverse("community:comment")
        post = Post.objects.first()
        offset = 1
        limit = 3

        self.authenticate()

        response = self.client.get(url + f"?post={post.id}&offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), limit)

        expected_comment_count = 1
        offset = self.comment_count - expected_comment_count
        limit = 3

        response = self.client.get(url + f"?post={post.id}&offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_comment_count)

        response = self.client.post(url, {"post": post.id, "content": "content"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url + f"?post={post.id}&offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_comment_count + 1)

    def test_board_failure(self):
        url = reverse("community:board")
        offset = 1
        limit = 3

        response = self.client.get(url + f"?offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_failure(self):
        url = reverse("community:post")

        self.authenticate()
        response = self.client.post(url, {"title": "title", "description": "description"})

        self.other_user_authenticate()
        response = self.client.patch(url + f"/{response.data['id']}",
                                     {"title": "title", "description": "description"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_failure(self):
        url = reverse("community:comment")

        self.authenticate()
        response = self.client.post(url, {"content": "content"})

        self.other_user_authenticate()
        response = self.client.patch(url + f"/{response.data['id']}", {"content": "content"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def authenticate(self):
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def other_user_authenticate(self):
        user = AuthUser.objects.create_user(
            username="test2",
            email="yyss6188@naver.com",
            password="password",
        )

        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
