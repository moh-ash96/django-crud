from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Snack

# Create your tests here.


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mohammad", email="mohammad@gmail.com", password="password"
        )

        self.snack = Snack.objects.create(
            title="Chocolate",
            description="Dark",
            purchaser=self.user,
        )


    def test_string_representation(self):
        self.assertEqual(str(self.snack), "Chocolate")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "Chocolate")
        self.assertEqual(f"{self.snack.description}", "Dark")
        self.assertEqual(f"{self.snack.purchaser}", "Mohammad")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chocolate")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/10/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Ordered By: Mohammad")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "shawerma",
                "description": "with mollases sauce",
                "purchaser": self.user.id,
            }, follow=True
        )
        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Order: shawerma")
    
    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)