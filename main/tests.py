from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from main.models import Articles


class ArticleTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test username', email='test@mail.com', password='Testpassword')

        self.author = User.objects.create(username="author_user")

        self.other_user = User.objects.create(username="other_user")

        self.article = Articles.objects.create(
            title="Test thread",
            intro="Intro",
            content="Text",
            date=timezone.now(),
            author=self.author
        )

        self.url = reverse("update_article", args=[self.article.pk])
    def test_article_max_length_validation(self):
        article = Articles.objects.create(title = "The quick brown fox jumps over the lazy dog. This sentence "
                                                       "contains every letter of the English alphabet and is often used "
                                                       "to test typewriters and computer keyboards. It is a classic "
                                                       "example of a pangram.",
                                               intro = "Space exploration has always captured the human imagination, "
                                                       "driving us to look beyond our own planet and wonder what "
                                                       "mysteries lie in the vast cosmos. From the early days of the "
                                                       "space race, when the first satellites were launched into orbit, "
                                                       "to the monumental achievement of landing astronauts on the moon, "
                                                       "our technological advancements have been nothing short of "
                                                       "extraordinary. Today, we have rovers traversing the dusty, red "
                                                       "surface of Mars, sending back high-resolution images and "
                                                       "analyzing soil samples to search for signs of past life."
                                                       "Meanwhile, powerful space telescopes gaze deep into the universe, "
                                                       "capturing light from distant galaxies that formed billions of "
                                                       "years ago. As we continue to develop new propulsion systems and "
                                                       "plan for potential manned missions to Mars and beyond, the dream "
                                                       "of becoming a multi-planetary species feels closer than ever before.",
                                               content = "content",
                                               date = timezone.now(),
                                               author = self.user,)

        with self.assertRaises(ValidationError):
            article.full_clean()


    def test_long_content_displays_on_details_page(self):
        long_text = (
            "Space exploration has always captured the human imagination, "
            "driving us to look beyond our own planet and wonder what "
            "mysteries lie in the vast cosmos. From the early days of the "
            "space race, when the first satellites were launched into orbit, "
            "to the monumental achievement of landing astronauts on the moon, "
            "our technological advancements have been nothing short of "
            "extraordinary. Today, we have rovers traversing the dusty, red "
            "surface of Mars, sending back high-resolution images."
        )
        article = Articles.objects.create(title = "Title",
                                               intro = "Intro",
                                               content = long_text,
                                               date = timezone.now(),
                                               author = self.user,)

        url = reverse("articles_detail", args=[article.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, long_text)

    def test_anonymous_user_is_redirected_to_login(self):
        url = reverse("article_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        expected_url = f"/login?next={url}"
        self.assertRedirects(response, expected_url)

    def test_author_can_access_update_page(self):
        self.client.force_login(self.author)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_author_cannot_access_update_page_when_not_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


