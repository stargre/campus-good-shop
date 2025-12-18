#!/usr/bin/env python
"""
诊断数据库查询问题
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from myapp.models import Product, Category, UserInfo
from myapp.serializers import ProductSerializer, CategorySerializer, UserInfoSerializer

print("=" * 60)
print("开始诊断数据库查询问题")
print("=" * 60)

# 测试1：查询Category
print("\n[测试1] 查询Category列表")
try:
    categories = Category.objects.all()
    print(f"✓ Category查询成功，总数: {categories.count()}")
    if categories.exists():
        cat = categories.first()
        print(f"  - 第一个分类: ID={cat.category_id}, Name={cat.category_name}")
except Exception as e:
    print(f"✗ Category查询失败: {e}")

# 测试2：查询Product
print("\n[测试2] 查询Product列表")
try:
    products = Product.objects.all()[:3]
    print(f"✓ Product查询成功")
    for p in products:
        print(f"  - Product ID={p.product_id}, Title={p.product_title}, cover_image_id={p.cover_image_id}")
except Exception as e:
    print(f"✗ Product查询失败: {e}")

# 测试3：序列化Category
print("\n[测试3] 序列化Category")
try:
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    print(f"✓ CategorySerializer成功，数据数: {len(serializer.data)}")
except Exception as e:
    print(f"✗ CategorySerializer失败: {e}")

# 测试4：序列化Product
print("\n[测试4] 序列化Product")
try:
    products = Product.objects.all()[:3]
    serializer = ProductSerializer(products, many=True)
    print(f"✓ ProductSerializer成功，数据数: {len(serializer.data)}")
    if serializer.data:
        print(f"  - 第一个商品: {list(serializer.data[0].keys())}")
except Exception as e:
    print(f"✗ ProductSerializer失败: {e}")
    import traceback
    traceback.print_exc()

# 测试5：查询UserInfo
print("\n[测试5] 查询UserInfo")
try:
    users = UserInfo.objects.all()[:3]
    print(f"✓ UserInfo查询成功，总数: {UserInfo.objects.count()}")
    for u in users:
        print(f"  - User ID={u.user_id}, Name={u.user_name}")
except Exception as e:
    print(f"✗ UserInfo查询失败: {e}")

# 测试6：序列化UserInfo
print("\n[测试6] 序列化UserInfo")
try:
    users = UserInfo.objects.all()[:1]
    serializer = UserInfoSerializer(users, many=True)
    print(f"✓ UserInfoSerializer成功")
except Exception as e:
    print(f"✗ UserInfoSerializer失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("诊断完成")
print("=" * 60)
