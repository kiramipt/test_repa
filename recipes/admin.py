from django.contrib import admin

from .models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "unit",)
    list_filter = ("title",)
    search_fields = ("title",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "color")


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "title", "image", "description",
                    "cooking_time", "pub_date")
    list_filter = ("title",)
    search_fields = ("title",)


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ("pk", "amount", "ingredient", "recipe")


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
