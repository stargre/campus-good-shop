-- =============================================
-- 校园二手交易平台数据库创建脚本
-- 文件名: db_create_mysql.sql
-- 描述: 创建校园二手交易平台的所有数据表结构
-- 作者: [你的名字]
-- 创建时间: [日期]
-- =============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS campus_shop;
USE campus_shop;

-- 首先删除所有表（如果存在），以确保干净的环境
-- 禁用外键检查，避免删除表时的外键约束错误
SET FOREIGN_KEY_CHECKS = 0;

-- 按依赖关系反向删除所有表（从最深层依赖开始）
DROP TABLE IF EXISTS b_error;      -- 错误日志表
DROP TABLE IF EXISTS b_op;         -- 操作日志表
DROP TABLE IF EXISTS b_login;      -- 登录日志表
DROP TABLE IF EXISTS b_notice;     -- 公告表
DROP TABLE IF EXISTS record;       -- 浏览记录表
DROP TABLE IF EXISTS reserve;      -- 预约表
DROP TABLE IF EXISTS comment;      -- 评论表
DROP TABLE IF EXISTS user_order;   -- 订单表
DROP TABLE IF EXISTS cart;         -- 购物车表
DROP TABLE IF EXISTS address;      -- 地址表
DROP TABLE IF EXISTS product_image;-- 商品图片表
DROP TABLE IF EXISTS product;      -- 商品表
DROP TABLE IF EXISTS category;     -- 商品分类表
DROP TABLE IF EXISTS user_info;    -- 用户信息表

-- 重新启用外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================
-- 开始创建表结构
-- 按照依赖关系顺序创建：先创建被引用的表，再创建引用其他表的表
-- =============================================

-- 1. 首先创建没有外键依赖的基础表
-- =============================================

-- 用户信息表：存储平台所有用户的基本信息
CREATE TABLE user_info (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID，主键',
    user_student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号，唯一标识',
    user_password VARCHAR(50) NOT NULL COMMENT '用户密码',
    user_name VARCHAR(20) NOT NULL COMMENT '用户真实姓名',
    user_collage VARCHAR(20) COMMENT '用户所在学院',
    user_email VARCHAR(100) UNIQUE NOT NULL COMMENT '用户邮箱，唯一',
    user_create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '用户注册时间',
    user_status TINYINT DEFAULT 1 COMMENT '用户状态：0-禁用，1-正常',
    user_avart VARCHAR(255) DEFAULT 'default-avatar.jpg' COMMENT '用户头像路径'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户基本信息表';

-- 商品分类表：存储商品分类信息
CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID，主键',
    category_name VARCHAR(50) UNIQUE NOT NULL COMMENT '分类名称，唯一',
    category_sort_order TINYINT DEFAULT 0 COMMENT '分类排序值，越小越靠前',
    category_create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '分类创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- 2. 创建有简单外键依赖的表
-- =============================================

-- 商品表：存储所有发布的商品信息
CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '商品ID，主键',
    user_id INT NOT NULL COMMENT '发布者用户ID',
    category INT NOT NULL COMMENT '商品分类ID',
    product_title VARCHAR(255) NOT NULL COMMENT '商品标题',
    product_o_price INT NOT NULL COMMENT '商品原价（单位：分）',
    product_price INT NOT NULL COMMENT '商品现价（单位：分）',
    product_status TINYINT NOT NULL DEFAULT 0 COMMENT '商品状态：0-待审核，1-审核通过，2-审核不通过，3-已售出',
    quality TINYINT DEFAULT 1 COMMENT '商品成色：1-全新，2-几乎全新，3-轻微使用痕迹，4-明显使用痕迹',
    reject_reason VARCHAR(255) COMMENT '审核不通过原因',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '商品创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '商品最后更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品信息表';

-- 为商品表添加外键约束
ALTER TABLE product 
ADD CONSTRAINT fk_product_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，商品发布者';

ALTER TABLE product 
ADD CONSTRAINT fk_product_category 
FOREIGN KEY (category) REFERENCES category(category_id)
COMMENT '关联分类表，商品所属分类';

-- 3. 创建依赖于商品表的其他表
-- =============================================

-- 商品图片表：存储商品的图片信息
CREATE TABLE product_image (
    image_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '图片ID，主键',
    product_id INT NOT NULL COMMENT '关联的商品ID',
    image_url VARCHAR(255) NOT NULL COMMENT '图片URL路径',
    sort_order TINYINT DEFAULT 0 COMMENT '图片排序，越小越靠前'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品图片表';

ALTER TABLE product_image 
ADD CONSTRAINT fk_product_image_product 
FOREIGN KEY (product_id) REFERENCES product(product_id)
COMMENT '关联商品表，图片所属商品';

-- 地址表：存储用户的收货地址信息
CREATE TABLE address (
    address_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '地址ID，主键',
    user_id INT NOT NULL COMMENT '关联的用户ID',
    receiver_name VARCHAR(50) NOT NULL COMMENT '收货人姓名',
    receiver_phone VARCHAR(20) NOT NULL COMMENT '收货人电话',
    receiver_address VARCHAR(255) NOT NULL COMMENT '详细收货地址',
    is_default TINYINT DEFAULT 0 COMMENT '是否默认地址：0-否，1-是'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户地址表';

ALTER TABLE address 
ADD CONSTRAINT fk_address_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，地址所属用户';

-- 购物车表：存储用户的购物车信息
CREATE TABLE cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '购物车项ID，主键',
    user_id INT NOT NULL COMMENT '关联的用户ID',
    product_id INT NOT NULL COMMENT '关联的商品ID',
    add_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '加入购物车时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户购物车表';

ALTER TABLE cart 
ADD CONSTRAINT fk_cart_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，购物车所属用户';

ALTER TABLE cart 
ADD CONSTRAINT fk_cart_product 
FOREIGN KEY (product_id) REFERENCES product(product_id)
COMMENT '关联商品表，购物车中的商品';

-- 订单表：存储交易订单信息
CREATE TABLE user_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID，主键',
    user_id INT NOT NULL COMMENT '买家用户ID',
    seller_id INT NOT NULL COMMENT '卖家用户ID',
    product_id INT NOT NULL COMMENT '关联的商品ID',
    product_title VARCHAR(255) NOT NULL COMMENT '商品标题（下单时的快照）',
    product_image VARCHAR(255) NOT NULL COMMENT '商品主图（下单时的快照）',
    price DECIMAL(10, 2) NOT NULL COMMENT '成交价格',
    order_status TINYINT NOT NULL COMMENT '订单状态：0-待支付，1-已支付，2-已发货，3-已完成，4-已取消，5-退款中',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '订单创建时间',
    pay_time TIMESTAMP NULL COMMENT '支付时间',
    receive_time TIMESTAMP NULL COMMENT '收货时间',
    cancel_time TIMESTAMP NULL COMMENT '取消时间',
    refund_reason VARCHAR(255) COMMENT '退款原因'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

ALTER TABLE user_order 
ADD CONSTRAINT fk_order_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，订单买家';

ALTER TABLE user_order 
ADD CONSTRAINT fk_order_seller 
FOREIGN KEY (seller_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，订单卖家';

ALTER TABLE user_order 
ADD CONSTRAINT fk_order_product 
FOREIGN KEY (product_id) REFERENCES product(product_id)
COMMENT '关联商品表，订单商品';

-- 4. 创建依赖于订单表的其他表
-- =============================================

-- 评论表：存储用户对交易的评价信息
CREATE TABLE comment (
    comment_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '评论ID，主键',
    order_id INT NOT NULL COMMENT '关联的订单ID',
    user_id INT NOT NULL COMMENT '评论用户ID（买家）',
    seller_id INT NOT NULL COMMENT '被评论的卖家ID',
    comment_content VARCHAR(1000) COMMENT '评论内容',
    rating TINYINT DEFAULT 10 COMMENT '评分：1-10分',
    comment_status TINYINT DEFAULT 0 COMMENT '评论状态：0-正常，1-隐藏',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '评论时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易评论表';

ALTER TABLE comment 
ADD CONSTRAINT fk_comment_order 
FOREIGN KEY (order_id) REFERENCES user_order(order_id)
COMMENT '关联订单表，评论所属订单';

ALTER TABLE comment 
ADD CONSTRAINT fk_comment_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，评论发布者';

ALTER TABLE comment 
ADD CONSTRAINT fk_comment_seller 
FOREIGN KEY (seller_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，被评论的卖家';

-- 预约表：存储线下交易预约信息
CREATE TABLE reserve (
    reserve_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '预约ID，主键',
    order_id INT NOT NULL COMMENT '关联的订单ID',
    user_id INT NOT NULL COMMENT '预约用户ID（买家）',
    seller_id INT NOT NULL COMMENT '卖家用户ID',
    address_id INT NOT NULL COMMENT '交易地址ID',
    reserve_status TINYINT DEFAULT 0 COMMENT '预约状态：0-待确认，1-已确认，2-已完成，3-已取消',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '预约创建时间',
    finish_time TIMESTAMP NULL COMMENT '预约完成时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='线下交易预约表';

ALTER TABLE reserve 
ADD CONSTRAINT fk_reserve_order 
FOREIGN KEY (order_id) REFERENCES user_order(order_id)
COMMENT '关联订单表，预约所属订单';

ALTER TABLE reserve 
ADD CONSTRAINT fk_reserve_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，预约用户';

ALTER TABLE reserve 
ADD CONSTRAINT fk_reserve_seller 
FOREIGN KEY (seller_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，被预约的卖家';

ALTER TABLE reserve 
ADD CONSTRAINT fk_reserve_address 
FOREIGN KEY (address_id) REFERENCES address(address_id)
COMMENT '关联地址表，交易地点';

-- 5. 创建其他辅助表
-- =============================================

-- 浏览记录表：存储用户的商品浏览历史
CREATE TABLE record (
    record_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID，主键',
    user_id INT NOT NULL COMMENT '用户ID',
    product_id INT NOT NULL COMMENT '商品ID',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '浏览时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户浏览记录表';

ALTER TABLE record 
ADD CONSTRAINT fk_record_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，浏览记录所属用户';

ALTER TABLE record 
ADD CONSTRAINT fk_record_product 
FOREIGN KEY (product_id) REFERENCES product(product_id)
COMMENT '关联商品表，被浏览的商品';

-- 公告表：存储系统公告信息
CREATE TABLE b_notice (
    b_notice_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '公告ID，主键',
    notice_content VARCHAR(1000) NOT NULL COMMENT '公告内容',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '公告发布时间',
    sort_value TINYINT DEFAULT 0 COMMENT '公告排序，越小越靠前'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统公告表';

-- 登录日志表：存储用户登录日志
CREATE TABLE b_login (
    b_login_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '登录记录ID，主键',
    user_id INT NOT NULL COMMENT '用户ID',
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '登录时间',
    ip_address VARCHAR(50) COMMENT '登录IP地址',
    login_device VARCHAR(100) COMMENT '登录设备信息',
    login_status BOOLEAN COMMENT '登录是否成功：true-成功，false-失败'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户登录日志表';

ALTER TABLE b_login 
ADD CONSTRAINT fk_login_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，登录用户';

-- 操作日志表：存储用户操作日志
CREATE TABLE b_op (
    b_op_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '操作记录ID，主键',
    user_id INT NOT NULL COMMENT '用户ID',
    op_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    op_type VARCHAR(20) COMMENT '操作类型',
    op_object VARCHAR(100) COMMENT '操作对象',
    op_detail TEXT COMMENT '操作详情'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户操作日志表';

ALTER TABLE b_op 
ADD CONSTRAINT fk_op_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，操作用户';

-- 错误日志表：存储系统错误日志
CREATE TABLE b_error (
    b_error_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '错误记录ID，主键',
    user_id INT NOT NULL COMMENT '用户ID（触发错误的用户）',
    error_type VARCHAR(50) NOT NULL COMMENT '错误类型',
    error_code TINYINT NOT NULL COMMENT '错误代码',
    error_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '错误发生时间',
    error_message TEXT NOT NULL COMMENT '错误信息',
    handle_status VARCHAR(20) NOT NULL DEFAULT '未处理' COMMENT '处理状态：未处理，已处理，忽略',
    handle_time TIMESTAMP NULL COMMENT '处理时间',
    handle_detail TEXT COMMENT '处理详情'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统错误日志表';

ALTER TABLE b_error 
ADD CONSTRAINT fk_error_user 
FOREIGN KEY (user_id) REFERENCES user_info(user_id)
COMMENT '关联用户表，触发错误的用户';

-- =============================================
-- 数据库创建完成
-- =============================================