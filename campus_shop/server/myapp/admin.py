from django.contrib import admin

# Register your models here.
from myapp.models import Category, Product, UserInfo, Comment, Tag, ProductTag

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserInfo)
admin.site.register(Tag)
admin.site.register(ProductTag)
admin.site.register(Comment)
