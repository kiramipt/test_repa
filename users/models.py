from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower",
        verbose_name="Подписчик")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following",
        verbose_name="Автор")

    class Meta:
        unique_together = ("follower", "following")


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_user",
        verbose_name="Автор")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_recipe",
        verbose_name="Любимые рецепты")


class Purchases(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchase_user",
        verbose_name="Автор")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="purchase_recipe",
        verbose_name="Покупки")

    class Meta:
        unique_together = ("user", "recipe",)
