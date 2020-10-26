import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from recipes.models import Recipe, User
from users.models import Favorite, Follow, Purchases


@login_required
def recipe_remove(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author and request.user.username == username:
        recipe.delete()
        return redirect("user_recipe_view_page", username)
    else:
        return redirect("recipe_view_page", username, recipe_id)


@login_required
@require_http_methods(["POST"])
def add_subscription(request):
    following = get_object_or_404(
        User,
        pk=json.loads(request.body)["id"]
    )
    Follow.objects.get_or_create(follower=request.user, following=following)
    return JsonResponse({"success": True})


@login_required
@require_http_methods(["DELETE"])
def remove_subscription(request, author_id):
    subscription = get_object_or_404(
        Follow, follower=request.user, following__pk=author_id)
    subscription.delete()
    return JsonResponse({"success": True})


@login_required
@require_http_methods(["POST"])
def add_favorites(request):
    recipe = get_object_or_404(Recipe, pk=json.loads(request.body)["id"])
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({"success": True})


@login_required
@require_http_methods(["DELETE"])
def remove_favorites(request, recipe_id):
    favorite_recipe = get_object_or_404(
        Favorite, user=request.user, recipe__pk=recipe_id)
    favorite_recipe.delete()
    return JsonResponse({"success": True})


@login_required
@require_http_methods(["POST"])
def add_purchase(request):
    recipe = get_object_or_404(Recipe, pk=json.loads(request.body).get("id"))
    Purchases.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({"success": True})


@login_required
@require_http_methods(["DELETE"])
def remove_purchase(request, recipe_id):
    get_object_or_404(Purchases, user=request.user,
                      recipe__pk=recipe_id).delete()
    return JsonResponse({"success": True})
