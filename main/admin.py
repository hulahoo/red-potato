from django.contrib import admin

from account.models import User
from main.models import Category, Product, ProductImage, Comment


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ('image', )


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    list_display = ('id', 'title')  # по нажатию мы переходим на сам продукт
    list_display_links = ('id', 'title')  # те поля с помощью которых можно попасть на описания продукта

admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
