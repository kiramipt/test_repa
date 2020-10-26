from django.contrib import admin

from .models import Favorite, Follow, Purchases


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "follower", "following",)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")


class PurchasesAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")


admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchases, PurchasesAdmin)
