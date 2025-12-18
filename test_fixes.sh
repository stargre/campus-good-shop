#!/bin/bash
# 快速测试修复

echo "正在重新启动服务..."

# 检查后端
cd server
echo "后端代码检查..."
python -m py_compile myapp/serializers.py myapp/views/index/product.py
if [ $? -eq 0 ]; then
    echo "✓ 后端代码无语法错误"
else
    echo "✗ 后端代码有语法错误"
    exit 1
fi

echo ""
echo "修复完成！现在请："
echo "1. 启动后端: python manage.py runserver 0.0.0.0:8000"
echo "2. 启动前端: npm run dev"
echo "3. 在浏览器硬刷新(Ctrl+Shift+R)后测试图片加载"
