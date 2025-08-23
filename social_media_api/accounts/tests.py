from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser, Follow

class FollowTests(APITestCase):
    def setUp(self):
        self.alice = CustomUser.objects.create_user(username="alice", password="pw")
        self.bob = CustomUser.objects.create_user(username="bob", password="pw")
        self.client.login(username="alice", password="pw")

    def test_follow_unfollow(self):
        resp = self.client.post(reverse("follow-user", args=[self.bob.id]))
        self.assertIn(resp.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.assertTrue(Follow.objects.filter(follower=self.alice, following=self.bob).exists())

        resp = self.client.post(reverse("unfollow-user", args=[self.bob.id]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.objects.filter(follower=self.alice, following=self.bob).exists())