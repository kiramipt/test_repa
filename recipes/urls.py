from django.urls import path

from . import views

urlpatterns = [
    path("", views.index,
         name="index"),
    path("recipe_new/", views.recipe_add_page,
         name="recipe_add_page"),
    path("subscription/", views.subscription,
         name="subscription"),
    path("favorites/", views.favorites,
         name="favorites"),
    path("purchases/", views.purchases_page,
         name="purchases_page"),
    path("purchases/download/", views.purchases_download,
         name="purchases_download"),
    path("<str:username>/", views.user_recipe_view_page,
         name="user_recipe_view_page"),
    path("<str:username>/<int:recipe_id>/", views.recipe_view_page,
         name="recipe_view_page"),
    path("<str:username>/<int:recipe_id>/edit/", views.recipe_edit_page,
         name="recipe_edit_page"),
]
