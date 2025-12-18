# 前言说明
校内闲置商品发布系统
已经进行项目的跑通，一些基础内容的修改，具体转化还有很多要修改 ：

修改清单：
+ 修改对应数据库，创建适配校内二手商品平台的数据表，并且插入数据（创建表和插入表的sql语句都要存储起来，方便后续管理）
+ 源代码是用mysql跑通的，修改成pgsql数据库（可选，也可以大家都用mysql，我先用了mysql跑通的
+ 将主页和后台的原来是菜品相关的内容修改成我们校园二手商品的内容（应该不多，主要看数据表创建的是什么样子的）
+ 实现后台的调用数据库逻辑（源代码这部分删去了，完整代码似乎要找他购买，我们应该能自己实现）
+ 稍微调整组件样式，修改一下页面样式（可选）


# Python Food 项目运行指南

## 一、环境要求

### 1. Python 环境
- Python 3.8
- pip 包管理器

### 2. 数据库环境
- MySQL 5.7 或更高版本
- 确保MySQL服务已启动

### 3. 前端环境（可选，如果需要运行前端）
- Node.js 16.14 或更高版本
- npm 或 yarn

---

## 二、后端运行步骤

### 步骤1：创建数据库

打开MySQL命令行或使用数据库管理工具，执行以下命令：

```sql
-- 创建数据库（注意：数据库名是 python_food，不是 shop）
CREATE DATABASE IF NOT EXISTS python_food DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

### 步骤2：导入SQL数据

```sql
-- 使用数据库
USE python_food;

-- 导入SQL文件（需要将路径替换为实际的SQL文件路径）
SOURCE D:/github/LocalResposity/Campus/python_food/python_food.sql;
```

或者使用命令行：

```bash
mysql -u root -p python_food < python_food.sql
```

### 步骤3：配置数据库连接

编辑 `server/server/settings.py` 文件，修改数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'python_food',  # 数据库名
        'USER': 'root',  # 数据库用户名（根据实际情况修改）
        'PASSWORD': '4643830',  # 数据库密码（根据实际情况修改）
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': '3306',  # 数据库端口
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    }
}
```

### 步骤4：安装Python依赖

在 `server` 目录下执行：

```bash
cd server
pip install -r requirements.txt
```

如果下载速度慢，可以使用国内镜像：

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
```

### 步骤5：确保upload目录存在

确保 `server/upload` 目录存在，如果不存在则创建：

```bash
# Windows
mkdir server\upload

# Linux/Mac
mkdir -p server/upload
```

创建必要的子目录：

```bash
mkdir server\upload\avatar
mkdir server\upload\cover
mkdir server\upload\banner
mkdir server\upload\ad
mkdir server\upload\img
```

### 步骤6：运行Django项目

在 `server` 目录下执行：

```bash
python manage.py runserver 0.0.0.0:8000
```

或者指定其他端口：

```bash
python manage.py runserver 0.0.0.0:9003
```

### 步骤7：验证运行

打开浏览器访问：
- Django管理后台：http://127.0.0.1:8000/admin/
- API接口测试：http://127.0.0.1:8000/myapp/index/classification/list

---

## 三、前端运行步骤（可选）

### 步骤1：安装依赖

在 `web` 目录下执行：

```bash
cd web
npm install
```

或使用yarn：

```bash
yarn install
```

### 步骤2：配置API地址

编辑 `web/src/store/constants.ts`，修改 `BASE_URL` 为后端API地址：

```typescript
export const BASE_URL = 'http://127.0.0.1:8000'
```

### 步骤3：运行前端项目

```bash
npm run dev
```

或：

```bash
yarn dev
```

### 步骤4：访问前端

打开浏览器访问：http://localhost:5173（默认端口）

---



## 五、数据库管理命令

### 删除数据库

```sql
DROP DATABASE IF EXISTS python_food;
```

### 创建数据库

```sql
CREATE DATABASE IF NOT EXISTS python_food DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

### 数据库备份

```bash
mysqldump -u root -p --databases python_food > python_food_backup.sql
```

### 数据库还原

```bash
mysql -u root -p python_food < python_food_backup.sql
```

### 创建管理员账号

```sql
-- 注意：密码需要使用MD5加密
INSERT INTO b_user(username, password, role, status) 
VALUES('admin123', MD5('admin123'), '0', '0');
```

---

## 六、开发建议

### 1. 使用虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 激活虚拟环境（Linux/Mac）
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```


## 八、项目结构说明

- `server/` - 后端Django项目
- `web/` - 前端Vue项目
- `python_food.sql` - 数据库SQL文件
- `项目架构文档.md` - 详细的项目架构说明

---

## 九、技术支持

如遇问题，可参考：
- `server/readme.md` - 后端部署说明
- `项目架构文档.md` - 项目架构文档
- Django官方文档：https://docs.djangoproject.com/
- Vue官方文档：https://vuejs.org/

