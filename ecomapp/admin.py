from django.contrib import admin

from .models import *



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title','slug']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register([Customer, Cart, CartProduct,Order,Product])