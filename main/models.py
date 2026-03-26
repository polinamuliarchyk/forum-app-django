from django.contrib.auth.models import User
from django.db import models

class Articles(models.Model):
    class Category(models.TextChoices):
        GENERAL = 'GEN', 'General'
        TECHNOLOGY = 'TECH', 'Technology'
        BOOKS = 'BOOK', 'Books'
        LIFESTYLE = 'LIFE', 'Lifestyle'
        HOBBIES = 'HOBB', 'Hobbies'

    title = models.CharField(max_length=100, verbose_name="Title")
    intro = models.TextField(max_length=500, verbose_name="Intro")
    content = models.TextField(verbose_name="Text")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    category = models.CharField(max_length=4, choices=Category.choices, default=Category.GENERAL, verbose_name="Category")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.pk}"

    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class Comment(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'