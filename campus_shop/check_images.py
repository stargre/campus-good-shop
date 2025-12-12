#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库中的图片信息
"""
import sys
import os
import django

# 配置Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from myapp.models import Product, ProductImage

print("=" * 80)
print("检查商品和图片数据")
print("=" * 80)

# 检查总数
product_count = Product.objects.count()
image_count = ProductImage.objects.count()
print(f"\n总商品数: {product_count}")
print(f"总图片数: {image_count}")

# 检查最新的5个商品
print("\n最新的5个商品:")
for p in Product.objects.order_by('-product_id')[:5]:
    images = ProductImage.objects.filter(product_id=p.product_id)
    print(f"\n商品ID: {p.product_id}")
    print(f"  标题: {p.product_title}")
    print(f"  cover_image_id: {p.cover_image_id}")
    print(f"  关联图片数: {images.count()}")
    for img in images:
        print(f"    - 图片ID: {img.image_id}, URL: {img.image_url}")

# 检查有cover_image_id但对应的ProductImage不存在的商品
print("\n检查数据一致性:")
products_with_cover_but_no_image = Product.objects.filter(
    cover_image_id__isnull=False
).exclude(
    productimage__image_id=django.db.models.F('cover_image_id')
)
print(f"cover_image_id指向不存在的ProductImage的商品数: {products_with_cover_but_no_image.count()}")
for p in products_with_cover_but_no_image[:3]:
    print(f"  - 商品ID: {p.product_id}, cover_image_id: {p.cover_image_id}")

# 检查无图片的商品
products_without_images = Product.objects.filter(productimage__isnull=True)
print(f"\n无图片的商品数: {products_without_images.count()}")

# 检查有图片但cover_image_id为空的商品
products_with_images_but_no_cover = Product.objects.filter(
    productimage__isnull=False,
    cover_image_id__isnull=True
).distinct()
print(f"有图片但cover_image_id为空的商品数: {products_with_images_but_no_cover.count()}")
for p in products_with_images_but_no_cover[:3]:
    images = ProductImage.objects.filter(product_id=p.product_id)
    print(f"  - 商品ID: {p.product_id}, 图片数: {images.count()}")

print("\n" + "=" * 80)
