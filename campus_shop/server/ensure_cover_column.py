#!/usr/bin/env python
"""
确保Product表有cover_image_id列
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # 首先检查列是否存在
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME='product' AND COLUMN_NAME='cover_image_id'
    """)
    result = cursor.fetchone()
    
    if result:
        print("✓ cover_image_id 列已存在")
    else:
        print("✗ cover_image_id 列不存在，正在添加...")
        try:
            cursor.execute("""
                ALTER TABLE product 
                ADD COLUMN cover_image_id INT NULL COMMENT '主图ID'
            """)
            print("✓ 成功添加cover_image_id列")
        except Exception as e:
            print(f"✗ 添加列失败: {e}")
    
    # 验证列的具体信息
    cursor.execute("""
        SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME='product' AND COLUMN_NAME='cover_image_id'
    """)
    col_info = cursor.fetchone()
    if col_info:
        col_name, col_type, is_nullable = col_info
        print(f"\n列信息:")
        print(f"  名称: {col_name}")
        print(f"  类型: {col_type}")
        print(f"  允许NULL: {is_nullable}")
