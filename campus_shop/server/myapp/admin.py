from django.contrib import admin

# Register your models here.
from myapp.models import Category, Product, UserInfo, Comment

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserInfo)
admin.site.register(Comment)
