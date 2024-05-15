from django.db import models
from apps.product.models import Product
from django.contrib.auth import get_user_model
from typing import List, Tuple

# Create your models here.

User = get_user_model()


class Comment(models.Model):
    body = models.TextField(verbose_name='Description')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}, {self.body}'


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f'{self.author} {self.rating}'


class Like(models.Model):
    # is_like = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.author}{self.product}'


class Dislike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='dislikes')

    def __str__(self):
        return f'{self.author}{self.product}'


class Favorites(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        ordering = ('-pk',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'product'], name='unique_author_product'),
        ]
        indexes = [
            models.Index(fields=['author', 'product'], name='index_author_product'),
        ]



