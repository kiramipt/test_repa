from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),

    path('about-author/', views.about_author, name='about-author'),
    path('about-spec/', views.about_spec, name='about-spec'),
]
