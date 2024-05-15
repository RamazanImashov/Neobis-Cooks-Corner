from django.db import models
from apps.recipe.models import Recipe
# from django.contrib.auth import get_user_model
from typing import List, Tuple
from apps.user_profile.models import UserProfile

# Create your models here.

User = UserProfile


class Comment(models.Model):
    body = models.TextField(verbose_name='Description')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}, {self.body}'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.author}{self.recipe}'


class Favorites(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        ordering = ('-pk',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'recipe'],
                name='unique_author_recipe'
            ),
        ]
        indexes = [
            models.Index(
                fields=['author', 'recipe'],
                name='index_author_recipe'
            ),
        ]



