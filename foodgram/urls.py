from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500 # noqa

handler404 = "recipes.views.page_not_found" # noqa
handler500 = "recipes.views.server_error" # noqa

urlpatterns = [
    path('about-author/', views.flatpage, {'url': '/about-author/'},
         name='about-author'),
    path("admin/", admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'},
         name='about-spec'),

    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),

    path("", include("recipes.urls")),
    path("", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
