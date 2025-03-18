from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import AuthUser
from community.models import Board, Post, Comment


class TestCommunity(APITestCase):
    def setUp(self):
        self.board_count = 5
        self.post_count = 5
        self.comment_count = 5

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
        url = reverse("community:board-list")
        offset = 1
        limit = 3

        self.authenticate()

        response = self.client.get(url + f"?offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), limit)

        expected_board_count = 1
        offset = self.board_count - expected_board_count
        limit = 3

        response = self.client.get(url + f"?offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), expected_board_count)

    def test_post_success(self):
        url = reverse("community:post-list")
        board = Board.objects.last()

        self.authenticate()

        response = self.client.get(url + f"?board={board.id}&offset=0&limit=3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

        response = self.client.post(url, {"board_id": board.id, "title": "New Post", "content": "content"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url + f"?board={board.id}&offset=0&limit=3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['title'], "New Post")

    def test_comment_success(self):
        url = reverse("community:comment-list")
        post = Post.objects.last()
        offset = 1
        limit = 3

        self.authenticate()

        response = self.client.get(url + f"?post={post.id}&offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), limit)

        response = self.client.post(url, {"post_id": post.id, "content": "new content"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url + f"?post={post.id}&offset=0&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), limit)
        self.assertEqual(response.data['results'][0]['content'], "new content")

    def test_board_failure(self):
        url = reverse("community:board-list")
        offset = 1
        limit = 3

        response = self.client.get(url + f"?offset={offset}&limit={limit}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_failure(self):
        url = reverse("community:post-list")
        board = Board.objects.last()

        self.authenticate()
        response = self.client.post(url, {"title": "title", "content": "description", "board_id": board.id})

        url = reverse("community:post-detail", args=[response.data['id']])
        self.other_user_authenticate()
        response = self.client.patch(url, {"title": "title", "content": "description"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_failure(self):
        url = reverse("community:comment-list")
        post = Post.objects.last()

        self.authenticate()
        response = self.client.post(url, {"content": "content", "post_id": post.id})

        url = reverse("community:comment-detail", args=[response.data['id']])
        self.other_user_authenticate()
        response = self.client.patch(url, {"content": "content"})
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
