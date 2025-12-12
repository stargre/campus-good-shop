# 数据库优化执行说明

## 已完成的代码修改

### 1. 模型定义修改 (models.py)
- ✅ 删除了 `Product.wish_count` 字段
- ✅ 删除了 `BOp` 模型类（操作日志表）
- ✅ 删除了 `BError` 模型类（错误日志表）
- ✅ 删除了 `Banner` 模型类（轮播图表）

### 2. 序列化器修改 (serializers.py)
- ✅ 移除了 `BOp, BError, Banner` 的模型导入
- ✅ 删除了 `BOpSerializer` 类
- ✅ 删除了 `BErrorSerializer` 类
- ✅ 删除了 `BannerSerializer` 类
- ✅ 删除了序列化器中的 `wish_count` 字段引用

### 3. 视图文件修改
- ✅ overview.py: 移除了 BError, BOp 导入
- ✅ utils.py: 移除了 BErrorSerializer 导入，log_error 函数改为空实现
- ✅ __init__.py (admin): 删除了 banner, opLog, errorLog 模块导入

### 4. URL 路由修改 (urls.py)
- ✅ 删除了所有 `/admin/banner/*` 路由
- ✅ banner、opLog、errorLog 的导入已在 __init__.py 中移除

### 5. 数据库迁移文件创建
- ✅ 创建了 `0009_delete_tables_and_fields.py` 迁移文件
  - 删除 Product.wish_count 字段
  - 删除 BOp 表
  - 删除 BError 表
  - 删除 Banner 表

---

## 执行步骤

### 步骤 1：应用迁移
在您的 Django 项目目录（`server` 文件夹）中，运行以下命令：

```bash
# 进入 server 目录（如果还未进入）
cd server

# 应用迁移
python manage.py migrate

# 或查看迁移状态
python manage.py migrate --plan
```

### 步骤 2：验证迁移
迁移完成后，可以通过以下命令验证：

```bash
# 查看已应用的迁移
python manage.py showmigrations

# 应该能看到 0009_delete_tables_and_fields 被标记为 [X]（已应用）
```

### 步骤 3：验证数据库
使用数据库工具（如 MySQL 客户端）检查表是否被正确删除：

```sql
-- 检查表是否存在（应该返回空）
SHOW TABLES LIKE 'b_error';  -- 应该为空
SHOW TABLES LIKE 'b_op';     -- 应该为空
SHOW TABLES LIKE 'banner';   -- 应该为空

-- 检查 product 表结构（wish_count 应该不存在）
DESCRIBE product;
-- 或
SHOW COLUMNS FROM product;
```

---

## 优化效果

### 删除的表
| 表名 | 记录数 | 用途 | 状态 |
|------|--------|------|------|
| b_error | 可能很多 | 错误日志（未被前端使用） | ✅ 已删除 |
| b_op | 可能很多 | 操作日志（未被前端使用） | ✅ 已删除 |
| banner | 可能较少 | 轮播图（完全未被使用） | ✅ 已删除 |

### 删除的字段
| 表 | 字段 | 状态 |
|----|------|------|
| product | wish_count | ✅ 已删除 |

### 数据库瘦身预期效果
- 表数量从 25 个减少到 **22 个**（减少 3 个）
- Product 表单行大小减少（删除一个 INT 字段）
- 数据库占用空间减少（特别是 b_error、b_op 表如果有大量记录）
- 更简洁的数据库结构

---

## 可能的注意事项

### ⚠️ 如果迁移失败

**可能原因 1：外键约束**
如果有其他表引用了被删除的表，迁移会失败。请检查是否有其他引用。

**解决方案：**
```python
# 如果有外键引用，可能需要先删除那些引用
# 在迁移中添加 operations 来处理这些依赖
```

**可能原因 2：迁移冲突**
如果您自己也创建了名为 0009 的迁移文件。

**解决方案：**
重命名您的迁移文件为 0010 或更高的数字，并修改依赖关系。

### ⚠️ 回滚迁移（如需要）

```bash
# 回滚到前一个迁移
python manage.py migrate myapp 0008_add_product_location

# 或检查迁移历史
python manage.py showmigrations myapp
```

---

## 备份建议

**强烈建议在执行迁移前备份数据库：**

```bash
# MySQL 备份
mysqldump -u root -p campus_shop > backup_$(date +%Y%m%d_%H%M%S).sql

# 或使用您的数据库管理工具进行备份
```

---

## 验证应用正常运行

迁移完成后，启动您的 Django 应用并检查：

```bash
# 启动开发服务器
python manage.py runserver

# 或运行测试
python manage.py test
```

检查以下功能是否正常：
- ✅ 用户登录/注册
- ✅ 商品发布/查询
- ✅ 订单管理
- ✅ 后台管理页面（应该看不到 banner、操作日志、错误日志菜单）

---

## 后续优化建议

### 1. 清理前端代码
检查前端是否有引用以下已删除项目的代码，如有应删除：
- Banner 组件（如果存在）
- 操作日志页面（如果存在）
- 错误日志页面（如果存在）

### 2. 监控数据库性能
迁移后监控数据库查询性能，确保删除这些表没有影响其他功能。

### 3. 考虑的额外优化
- **Record 表：** 浏览记录表使用频率低，如不需要推荐功能可考虑定期清理或删除
- **Cart 表：** 购物车功能较简单，可考虑优化查询索引
- **Reserve 表：** 确保预约流程完整实现以利用所有字段

---

## 总结

✅ **所有代码修改已完成**
✅ **迁移文件已创建**
🔄 **下一步：执行迁移**

运行 `python manage.py migrate` 即可完成数据库优化！

