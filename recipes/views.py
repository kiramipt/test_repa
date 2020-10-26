from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Ingredient, IngredientAmount, Recipe
from .utils import get_favorites, get_ingredients

User = get_user_model()


def index(request):

    tags = request.GET.get("tags", "")

    if tags:
        recipes = Recipe.objects.filter(
            tags__slug__in=tags.split(",")
        ).select_related(
            "author"
        ).prefetch_related(
            "tags"
        ).distinct()
    else:
        recipes = Recipe.objects.all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        favorites = get_favorites(request)
        purchases = Recipe.objects.filter(
            purchase_recipe__user=request.user)
    else:
        favorites, purchases = [], []

    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "tags": tags,
        "favorites": favorites,
        "purchases": purchases,
        "is_index_page": True,
    })


@login_required
def subscription(request):
    user = request.user
    authors = User.objects.filter(
        following__follower=user).prefetch_related("recipes").order_by('-id')

    paginator = Paginator(authors, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "subscription.html", {
        "page": page,
        "paginator": paginator,
        "is_subscription_page": True,
    })


@login_required
def favorites(request):

    tags = request.GET.get("tags", "")

    if tags:
        recipes = Recipe.objects.filter(
            favorite_recipe__user=request.user
        ).filter(
            tags__slug__in=tags.split(",")
        ).distinct()
    else:
        recipes = Recipe.objects.filter(
            favorite_recipe__user=request.user
        )

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    favorites = get_favorites(request)
    purchases = Recipe.objects.filter(purchase_recipe__user=request.user)

    return render(request, "favorites.html", {
        "page": page,
        "paginator": paginator,
        "tags": tags,
        "favorites": favorites,
        "purchases": purchases,
        "is_favorites_page": True,
    })


def user_recipe_view_page(request, username):

    tags = request.GET.get("tags", "")
    author = get_object_or_404(User, username=username)

    if tags:
        recipes = Recipe.objects.filter(
            author_id=author.id
        ).filter(
            tags__slug__in=tags.split(",")
        ).distinct()
    else:
        recipes = Recipe.objects.filter(author_id=author.id)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        favorites = get_favorites(request)
        purchases = Recipe.objects.filter(
            purchase_recipe__user=request.user)
    else:
        favorites, purchases = [], []

    return render(request, "user_recipe_view_page.html", {
        "page": page,
        "paginator": paginator,
        "author": author,
        "tags": tags,
        "favorites": favorites,
        "purchases": purchases,
    })


def recipe_view_page(request, username, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    ingredients = IngredientAmount.objects.filter(recipe_id=recipe_id)
    author = get_object_or_404(User, username=username)

    if request.user.is_authenticated:
        favorites = get_favorites(request)
        purchases = Recipe.objects.filter(
            purchase_recipe__user=request.user)
    else:
        favorites, purchases = [], []

    return render(request, "recipe_view_page.html", {
        "author": author,
        "recipe": recipe,
        "ingredients": ingredients,
        "favorites": favorites,
        "purchases": purchases,
    })


@login_required
def recipe_edit_page(request, username, recipe_id):

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author or username != request.user.username:
        return redirect("recipe_view_page",
                        username=recipe.author, recipe_id=recipe.pk)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredients = get_ingredients(request)

        if not bool(ingredients):
            form.add_error(None, "Добавьте хотя бы один ингредиент")

        elif form.is_valid():
            form.save()
            recipe.ingredientamount_set.all().delete()
            ingredient_amounts = [
                IngredientAmount(
                    amount=amount,
                    ingredient=get_object_or_404(Ingredient, title=title),
                    recipe=recipe
                ) for title, amount in ingredients.items()
            ]
            IngredientAmount.objects.bulk_create(ingredient_amounts)
            return redirect("recipe_view_page",
                            username=recipe.author, recipe_id=recipe.pk)

    form = RecipeForm(instance=recipe)
    ingredients = IngredientAmount.objects.filter(recipe_id=recipe_id)

    return render(request, "recipe_edit_page.html",
                  {"form": form, "recipe": recipe, "ingredients": ingredients})


@login_required
def recipe_add_page(request):

    if request.method == "POST":
        form = RecipeForm(request.POST, files=request.FILES)
        ingredients = get_ingredients(request)

        if not bool(ingredients):
            form.add_error(None, "Добавьте хотя бы один ингредиент")

        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            ingredient_amounts = [
                IngredientAmount(
                    amount=amount,
                    ingredient=get_object_or_404(Ingredient, title=title),
                    recipe=recipe
                ) for title, amount in ingredients.items()
            ]

            IngredientAmount.objects.bulk_create(ingredient_amounts)
            form.save_m2m()
            return redirect("recipe_view_page",
                            username=request.user, recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, "recipe_add_page.html",
                  context={"form": form, "is_recipe_new_page": True})


@login_required
def purchases_page(request):
    recipes = Recipe.objects.filter(purchase_recipe__user=request.user)
    return render(request, "purchases_page.html",
                  {"recipes": recipes, "is_purchases_page": True})


@login_required
def purchases_download(request):

    recipes = Recipe.objects.filter(purchase_recipe__user=request.user)
    ingredients = recipes.annotate(
        name=F("ingredient__title"),
        dimension=F("ingredient__unit")
    ).values("name", "dimension").annotate(
        total=Sum("ingredientamount__amount")).order_by("name")

    res = ["name | dimension | total"]
    for ingredient in ingredients[1:]:
        name = ingredient["name"]
        dimension = ingredient["dimension"].replace("\r", "")
        total = ingredient["total"]
        res.append(f"{name} | {dimension} | {total}")

    response = HttpResponse("\n".join(res), content_type="text/txt")
    response["Content-Disposition"] = "attachment; filename='purchases.txt'"

    return response


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        "misc/500.html",
        status=500
    )
