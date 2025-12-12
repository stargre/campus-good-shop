# 前端API使用与后端数据库审计报告

## 一、前端使用的所有后端API端点清单

### 1. 索引（前台）模块：`/index/`

#### 1.1 用户相关 (`/index/user/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `userLoginApi` | `/index/user/login` | POST | user.login | UserInfo, BLogin | 用户登录，记录登录日志 |
| `userRegisterApi` | `/index/user/register` | POST | user.register | UserInfo | 用户注册 |
| `detailApi` | `/index/user/info` | GET | user.info | UserInfo | 获取当前用户信息 |
| `updateUserInfoApi` | `/index/user/update` | POST | user.update | UserInfo, ProductImage(头像) | 更新用户信息和头像 |
| `updateUserPwdApi` | `/index/user/updatePwd` | POST | user.updatePwd | UserInfo | 修改密码 |

#### 1.2 商品相关 (`/index/product/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `getProductList` | `/index/product/list` | GET | product.list | Product, Category | 分页查询商品列表 |
| `getProductDetail` | `/index/product/detail` | GET | product.detail | Product, ProductImage, Record, UserInfo | 获取商品详情，记录浏览 |
| `createProduct` | `/index/product/create` | POST | product.create | Product, ProductImage | 创建商品 |
| `updateProduct` | `/index/product/update` | POST | product.update | Product, ProductImage | 更新商品 |
| `deleteProduct` | `/index/product/delete` | POST | product.delete | Product, ProductImage | 删除商品 |
| `getMyProductList` | `/index/product/myList` | GET | product.myList | Product | 查询当前用户发布的商品 |
| `reserveProductApi` | `/index/product/reserve` | POST | product.reserve | Product, Reserve, Address, UserInfo | 预约商品 |
| `cancelReserve` | `/index/product/cancel_reserve` | POST | product.cancel_reserve | Product, Reserve | 取消预约 |

#### 1.3 订单相关 (`/index/order/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `getOrderList` | `/index/order/list` | GET | order.list_api | UserOrder | 查询订单列表（买家或卖家） |
| `getOrderDetail` | `/index/order/detail` | GET | order.detail_api | UserOrder, Product, ProductImage | 查询订单详情 |
| `createOrder` | `/index/order/create` | POST | order.create | UserOrder, Product, ProductImage | 创建订单 |
| `payOrder` | `/index/order/pay` | POST | order.pay | UserOrder, Product | 支付订单 |
| `confirmOrderReceipt` | `/index/order/confirm` | POST | order.confirm_receipt | UserOrder | 确认收货 |
| `cancelOrder` | `/index/order/cancel_order` | POST | order.cancel_order | UserOrder, Product | 取消订单 |
| `evaluateOrder` | `/index/order/evaluate` | POST | order.evaluate | UserOrder, Comment, UserInfo | 评价订单 |
| `deliverOrder` | `/index/order/deliver` | POST | order.deliver | UserOrder | 发货（卖家） |

#### 1.4 评论相关 (`/index/comment/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `createApi` | `/index/comment/create` | POST | comment.create | Comment, Product, UserInfo | 创建评论 |
| `listProductCommentsApi` | `/index/comment/list` | GET | comment.list_api | Comment, Product | 获取商品评论列表 |
| `listUserCommentsApi` | `/index/comment/myList` | GET | comment.list_my_comment | Comment | 获取用户自己的评论 |
| `likeApi` | `/index/comment/like` | POST | comment.like | Comment | 评论点赞 |
| `deleteApi` | `/index/comment/delete` | POST | comment.delete | Comment | 删除评论 |

#### 1.5 地址相关 (`/index/address/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `listApi` (address) | `/index/address/list` | GET | address.list_api | Address | 查询用户地址列表 |
| `createApi` (address) | `/index/address/create` | POST | address.create | Address, UserInfo | 创建地址 |
| `updateApi` | `/index/address/update` | POST | address.update | Address, UserInfo | 更新地址 |
| `deleteApi` (address) | `/index/address/delete` | POST | address.delete | Address | 删除地址 |

#### 1.6 收藏相关 (`/index/favorite/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `addProductCollectUserApi` | `/index/favorite/add` | POST | favorite.add | Favorite, Product, UserInfo | 添加收藏 |
| `removeProductCollectUserApi` | `/index/favorite/remove` | POST | favorite.remove | Favorite, UserInfo | 移除收藏 |
| `batchRemove` | `/index/favorite/batchRemove` | POST | favorite.batchRemove | Favorite, UserInfo | 批量移除收藏 |
| `getUserCollectListApi` | `/index/favorite/list` | GET | favorite.list | Favorite, Product | 获取收藏列表 |

#### 1.7 购物车相关 (`/index/cart/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `list_api` (cart) | `/index/cart/list` | GET | cart.list_api | Cart, Product, ProductImage | 查询购物车 |
| `add` (cart) | `/index/cart/add` | POST | cart.add | Cart, Product, UserInfo | 添加到购物车 |
| `delete` (cart) | `/index/cart/delete` | POST | cart.delete | Cart, UserInfo | 删除购物车项 |
| `deleteAll` | `/index/cart/deleteAll` | POST | cart.deleteAll | Cart, UserInfo | 清空购物车 |

#### 1.8 分类相关 (`/index/category/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `list_api` (category) | `/index/category/list` | GET | category.list_api | Category | 获取分类列表 |
| `detail` (category) | `/index/category/detail` | GET | category.detail | Category | 获取单个分类 |
| `listWithProducts` | `/index/category/listWithProducts` | GET | category.listWithProducts | Category, Product | 获取分类及其商品 |

#### 1.9 浏览记录相关 (`/index/record/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| 隐式（在product.detail中） | `/index/record/create` | GET | record.create | Record, Product, UserInfo | 创建浏览记录 |
| `list_api` (record) | `/index/record/list` | GET | record.list_api | Record, Product | 获取用户浏览记录 |
| `delete` (record) | `/index/record/delete` | POST | record.delete | Record, UserInfo | 删除浏览记录 |
| `deleteAll` (record) | `/index/record/deleteAll` | POST | record.deleteAll | Record, UserInfo | 清空浏览记录 |

#### 1.10 搜索相关 (`/index/search/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| 页面嵌入 | `/index/search/search` | GET | search.search | Product, Category | 搜索商品 |
| 页面嵌入 | `/index/search/hotKeywords` | GET | search.hotKeywords | (无DB访问) | 获取热门关键词 |

#### 1.11 上传相关 (`/index/upload/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `uploadImageApi` | `/index/upload/image` | POST | upload.image | (文件系统) | 上传图片 |

#### 1.12 公告相关 (`/index/notice/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `listApi` (notice) | `/index/notice/list` (或 `/index/notice/list_api`) | GET | notice.list_api | BNotice | 获取公告列表 |

---

### 2. 后台管理模块：`/admin/`

#### 2.1 概览相关 (`/admin/overview/`)
| 前端调用 | 后端端点 | HTTP方法 | 后端视图 | 使用的表 | 说明 |
|---------|---------|---------|---------|----------|------|
| `listApi` (overview) | `/admin/overview/count` | GET | overview.count | Product, UserOrder, Comment, Category, UserInfo, BLogin | 获取统计数据 |
| `sysInfoApi` | `/admin/overview/sysInfo` | GET | overview.sysInfo | (系统信息，不涉及业务表) | 获取系统信息 |

#### 2.2 其他后台模块（未详细列出，但存在）
- `/admin/user/` - 用户管理
- `/admin/product/` - 商品管理
- `/admin/order/` - 订单管理
- `/admin/comment/` - 评论管理
- `/admin/category/` - 分类管理
- `/admin/notice/` - 公告管理
- `/admin/banner/` - 轮播图管理
- `/admin/log/` - 日志管理（loginLog, errorLog, opLog）

---

## 二、使用的数据库表统计

### 前端直接使用的表（通过前端API）

| 表名 | 中文名 | 使用频率 | 被使用的场景 | 被访问的字段示例 |
|------|--------|---------|-----------|-------------------|
| **UserInfo** | 用户信息表 | 🔴 高 | 登录、注册、用户信息管理、订单、评论等 | user_id, user_name, user_email, user_password, token, user_avart, user_mobile, user_collage |
| **Product** | 商品表 | 🔴 高 | 商品查询、发布、更新、删除、订单、评论、浏览等 | product_id, product_title, product_price, product_status, category, user_id, view_count, collect_count, location, quality, content, create_time |
| **Category** | 分类表 | 🟠 中 | 分类查询、商品筛选 | category_id, category_name |
| **ProductImage** | 商品图片表 | 🟠 中 | 商品图片管理、展示 | image_id, product_id, image_url, sort_order |
| **UserOrder** | 订单表 | 🟠 中 | 订单创建、查询、支付、发货、确认收货 | order_id, user_id, seller_id, product_id, order_status, price, create_time, pay_time, receive_time |
| **Comment** | 评论表 | 🟠 中 | 评论创建、查询、点赞 | comment_id, product_id, user_id, seller_id, comment_content, rating, like_count, create_time |
| **Address** | 地址表 | 🟠 中 | 收货地址管理（预约、订单配送） | address_id, user_id, receiver_name, receiver_phone, receiver_address, is_default |
| **Favorite** | 收藏表 | 🟠 中 | 收藏管理 | favorite_id, user_id, product_id, create_time |
| **Record** | 浏览记录表 | 🟡 低 | 记录用户浏览历史、推荐（可选） | record_id, user_id, product_id, create_time |
| **Cart** | 购物车表 | 🟡 低 | 购物车管理 | cart_id, user_id, product_id, add_time |
| **BNotice** | 公告表 | 🟡 低 | 系统公告显示 | b_notice_id, notice_content, create_time |
| **Reserve** | 预约表 | 🟡 低 | 商品预约管理 | reserve_id, product_id, user_id, seller_id, reserve_status, reserve_time, trade_location, remark |
| **BLogin** | 登录日志表 | 🟡 低 | 登录日志记录 | b_login_id, user_id, login_time, ip_address, login_device, login_status |

### 前端未直接使用的表（后台管理或内部使用）

| 表名 | 中文名 | 使用情况 | 用途 |
|------|--------|---------|------|
| **BError** | 错误日志表 | ❌ 未被前端API使用 | 系统错误日志（后台查看或日志系统使用） |
| **BOp** | 操作日志表 | ❌ 未被前端API使用 | 用户操作审计日志 |
| **Banner** | 轮播图表 | ⚠️ 部分使用 | 首页轮播图（前台可能有相关API，但未在现有API列表中找到） |

---

## 三、未被前端使用的后端表和字段

### 3.1 完全未使用的表
1. **BError** - 错误日志表
   - 说明：虽然定义了，但前端没有相关API调用
   - 用途：用于记录系统错误，可能由后台管理员查看

2. **BOp** - 操作日志表
   - 说明：虽然定义了，但前端没有相关API调用
   - 用途：用于记录用户操作日志，可能用于审计

3. **Banner** - 轮播图表
   - 说明：定义了但前端找不到直接的API调用
   - 可能原因：轮播图可能由其他方式管理或在初始化时加载

### 3.2 定义但基本未使用的字段

#### Product 表
- `wish_count` - 心愿次数（已定义但未在任何视图中使用）

#### UserInfo 表
- `user_create_time` - 注册时间（已获取但前端可能未显示）

#### UserOrder 表
- `refund_reason` - 退款原因（已定义但未被evaluate接口使用）
- `deliver_time` - 发货时间（后来才添加）

#### Reserve 表
- 许多新增字段（remark, trade_location等）虽然已支持但可能未被所有流程使用

---

## 四、数据库优化建议

### 4.1 可以删除的表（完全未使用）
```
- BError：如果没有系统级错误日志需求，可删除
- BOp：如果没有操作审计需求，可删除
```

### 4.2 可以删除的字段（几乎未使用）
```
Product 表：
  - wish_count：未在任何地方使用，可删除

UserOrder 表：
  - refund_reason：仅用于展示，如不需要可删除
```

### 4.3 可以优化的地方
```
1. Record 表：
   - 该表用于记录用户浏览历史，但前端使用频率低
   - 建议：如不需要推荐功能，可考虑定期清理或删除

2. Cart 表：
   - 购物车功能较为简单（仅添加/删除）
   - 建议：可集成到Order中或保持轻量级设计

3. Reserve 表：
   - 预约功能新增了多个字段但使用不完整
   - 建议：完成预约流程的完整实现
```

### 4.4 建议保留的表
所有主要业务表（Product, UserInfo, UserOrder, Comment, Category, ProductImage, Address等）都在活跃使用中，建议保留。

---

## 五、前端功能覆盖度统计

### 已实现并调用的功能
✅ 用户登录/注册  
✅ 商品列表/详情/发布/编辑/删除  
✅ 订单创建/支付/确认收货/评价  
✅ 评论创建/查看/点赞  
✅ 地址管理  
✅ 收藏管理  
✅ 购物车管理  
✅ 分类查询  
✅ 浏览记录（部分）  
✅ 商品预约  

### 后端存在但前端可能未完全使用的功能
⚠️ 预约功能（reserve表字段较多，前端使用可能不完整）  
⚠️ 轮播图管理（Banner表存在但未找到前端API）  
⚠️ 错误日志查询（BError表存在但无前端API）  
⚠️ 操作日志查询（BOp表存在但无前端API）  

---

## 六、总结

**前端已使用的表：** 12个（UserInfo, Product, Category, ProductImage, UserOrder, Comment, Address, Favorite, Record, Cart, BNotice, Reserve）

**前端未使用的表：** 3个（BError, BOp, Banner可能部分使用）

**建议清理项：**
1. 删除完全未使用的表：BError, BOp
2. 删除未使用的字段：Product.wish_count
3. 补完预约功能（现有代码支持但前端调用不完整）
4. 检查轮播图功能是否需要前端API支持

**数据库瘦身后的表数量：** 14 → 12 表（删除 BError, BOp）

---

**报告生成时间：** 2024年  
**审计范围：** 前端API调用 → 后端视图 → 数据库表映射  
**审计工具：** 代码分析与手工审查
