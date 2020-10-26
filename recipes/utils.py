from users.models import Favorite

from .models import Recipe


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith("nameIngredient"):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                "valueIngredient_" + value_ingredient]
    return ingredients


def get_favorites(request):
    favorites = []
    if request.user.is_authenticated:

        favorites = list(Favorite.objects.filter(
            user=request.user
        ).values_list("recipe_id", flat=True))

    return favorites


def get_purchases_count(request):
    purchases_count = 0
    if request.user.is_authenticated:
        purchases_count = Recipe.objects.filter(
            purchase_recipe__user=request.user
        ).count()

    return {"purchases_count": purchases_count}


def get_followings(request):
    if request.user.is_authenticated:
        return {"followings": request.user.follower.values_list(
            "following_id", flat=True
        )}
    else:
        return {}
