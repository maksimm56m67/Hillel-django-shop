from django.contrib import admin
from items.models import Item, Category, FavoriteProduct
from django.utils.safestring import mark_safe
from shop.mixins.admin_mixins import ImageSnapshotAdminMixin

@admin.register(Item)
class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at', 'total_price')

    

    
@admin.register(Category)
class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    ...

@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'items')

