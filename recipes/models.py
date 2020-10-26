from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    unit = models.CharField(max_length=255, verbose_name="Мера измерения")

    def __str__(self):
        return self.title


class IngredientAmount(models.Model):
    amount = models.IntegerField(verbose_name="Кол-во")
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)


class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    color = models.CharField(max_length=255, verbose_name="Цвет")

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(upload_to="image/", verbose_name="Путь до файла")
    description = models.TextField(verbose_name="Описание")
    ingredient = models.ManyToManyField(
        Ingredient, through=IngredientAmount
    )
    tags = models.ManyToManyField(Tag, related_name="recipes")
    cooking_time = models.IntegerField(
        default=10, verbose_name="Время приготовления")
    pub_date = models.DateTimeField(
        "date published", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-pub_date", )
