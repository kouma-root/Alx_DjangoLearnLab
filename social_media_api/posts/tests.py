from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import CustomUser, Follow
from posts.models import Post

class FeedTests(APITestCase):
    def setUp(self):
        self.alice = CustomUser.objects.create_user(username="alice", password="pw")
        self.bob = CustomUser.objects.create_user(username="bob", password="pw")
        self.client.login(username="alice", password="pw")
        Follow.objects.create(follower=self.alice, following=self.bob)
        Post.objects.create(author=self.bob, title="Hi", content="From Bob")

    def test_feed_shows_followed_posts(self):
        resp = self.client.get(reverse("feed"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["results"][0]["title"], "Hi")