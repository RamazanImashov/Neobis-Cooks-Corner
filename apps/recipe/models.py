from django.db import models
import os, uuid
from pytils.translit import slugify
from apps.user_profile.models import UserProfile

# Create your models here.


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(instance.directory_string_var, filename)


class Recipe(models.Model):
    slug = models.SlugField(primary_key=True, null=False, blank=True, unique=True, verbose_name="Слаг")
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="recipe", verbose_name="id пользователя")
    recipe_name = models.CharField(max_length=255, blank=False, null=False, verbose_name="Название рецепта")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    DIFFICULTY_CHOICE = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hurd", "Hurd"),
    ]
    difficulty = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=DIFFICULTY_CHOICE,
        verbose_name="Сложность приготовление")
    CATEGORY_CHOICE = [
        ("Breakfast", "Breakfast"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
    ]
    category = models.CharField(max_length=20, blank=False, null=False, choices=CATEGORY_CHOICE, verbose_name="Категория блюда")
    preparation_time = models.CharField(max_length=20, null=False, blank=True, verbose_name="Приблизительное время")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.recipe_name)
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.slug} {self.recipe_name}'


class AddRecipeImage(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_image")
    image = models.ImageField(upload_to="hello")
    directory_string_var = f'Recipe-Image'


class AddRecipeIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_ingredient")
    ingredient_name = models.CharField(max_length=255, blank=False, null=False, verbose_name="Название ингредиента")
    amount = models.PositiveIntegerField()
    UNIT_CHOICE = [
        ("кг", "Килограммы"),
        ("г", "Граммы"),
        ("л", "Литры"),
        ("мл", "Миллилитры"),
        ("ч.л.", "Чайные ложки "),
        ("ст.л.", "Столовые ложки"),
        ("шт", "Штук"),
    ]
    unit = models.CharField(max_length=255, blank=False, null=False, choices=UNIT_CHOICE, verbose_name="Единицы измерения")
