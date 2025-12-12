## 环境与启动
- 后端（Conda py38）：
  - `conda deactivate`
  - `conda activate py38`
  - 进入后端：`d:\github\LocalResposity\Campus\campus_shop\campus_shop\server`
  - `pip install -r requirements.txt`
  - 确认 MySQL `campus_shop` 可用且已导入 `campus_schema.sql` 与 `insert_data.sql`。
  - `python manage.py runserver 0.0.0.0:8000`
- 前端（Conda test）：
  - `conda deactivate`
  - `conda activate test`
  - 进入前端：`d:\github\LocalResposity\Campus\campus_shop\campus_shop\web`
  - `npm install`
  - `npm run dev`
  - 保证 `BASE_URL='http://127.0.0.1:8000/myapp'` 与 test 环境一致（使用 `.env`/常量文件）。

## 直接改代码以跑通功能
- 数据层：仅轻校对（不重写），必要时为兼容接口补充索引/字段默认值。
- 后端改造：
  - 修正与旧“菜品系统”相关的路由/视图/序列化器字段与文案。
  - 对照前端 API 封装，统一所有端点路径与参数；补全缺失的校验或默认值。
  - 解决可能的迁移/模型与现有表结构的差异，优先保证读写成功。
- 前端改造：
  - 将所有“菜品/点餐”等旧词替换为“二手商品交易系统”，统一菜单、标题与提示文案。
  - 校对与后端一致的 `BASE_URL`、请求头（`TOKEN`/`ADMINTOKEN`）、分页与筛选参数。
  - 修复页面流程：登录/发帖/浏览/收藏/购物车/下单/预约/评价主流程与后台管理。
- UI 与图表：
  - 微调主题配色、列表卡片式、详情图片画廊。
  - 用 ECharts 替换统计图并与后台数据对齐。

## 验证清单（依据《第14组_校内闲置商品发布系统.docx》）
- 用户：注册/登录，令牌注入，请求成功；默认地址读取。
- 分类/商品：分类列表/详情，商品列表/详情（图片、成色、描述），发布/编辑/删除商品。
- 收藏/购物车：新增/移除/批量，列表与数量同步。
- 订单：创建/取消/支付/确认收货，状态与时间戳正确；订单详情快照字段正确。
- 预约：创建/完成/取消；时间与地点字段写入正确。
- 评论：发表/列表/我的评论；（如有）点赞计数变更。
- 公告/日志/轮播图：后台维护并前台展示与跳转。

## 交付
- 完整可运行的项目（数据库→后端→前端）；
- 改动清单与联调报告；UI 变更说明与预览。

请确认该方案，我将立刻按此在 py38 与 test 两套 Conda 环境下直接改代码并跑通所有功能。