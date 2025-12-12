-- 数据插入脚本表

-- Dumping data for table `address`
--
LOCK TABLES `address` WRITE;
INSERT INTO `address` VALUES 
(1,'系统管理员','13800000017','信息中心宿舍楼 3栋320室',1,1),
(2,'张三','13800000034','计算机学院宿舍楼 10栋289室',1,2),
(3,'李四','13800000051','电子工程学院宿舍楼 3栋206室',1,3),
(4,'王五','13800000068','文学院宿舍楼 1栋126室',1,4),
(5,'赵六','13800000085','经济管理学院宿舍楼 4栋242室',1,5),
(6,'小美','13800000102','艺术设计学院宿舍楼 4栋168室',1,6),
(8,'zhiyu Lin','15305977777','Sichuan',0,8),
(9,'zhiyu Lin','15305977276','Sichuan',0,1);
UNLOCK TABLES;

--
-- Dumping data for table `auth_group`
--
LOCK TABLES `auth_group` WRITE;
INSERT INTO `auth_group` VALUES 
(3,'卖家组'),
(2,'学生组'),
(1,'管理员组');
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--
LOCK TABLES `auth_group_permissions` WRITE;
INSERT INTO `auth_group_permissions` VALUES 
(1,1,1),(2,1,2),(3,1,3),(4,2,3),(5,2,5);
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--
LOCK TABLES `auth_permission` WRITE;
INSERT INTO `auth_permission` VALUES 
(1,'Can add product',2,'add_product'),
(2,'Can change product',2,'change_product'),
(3,'Can view product',2,'view_product'),
(4,'Can add order',4,'add_order'),
(5,'Can change order',4,'change_order'),
(6,'Can add log entry',7,'add_logentry'),
(7,'Can change log entry',7,'change_logentry'),
(8,'Can delete log entry',7,'delete_logentry'),
(9,'Can view log entry',7,'view_logentry'),
(10,'Can add permission',8,'add_permission'),
(11,'Can change permission',8,'change_permission'),
(12,'Can delete permission',8,'delete_permission'),
(13,'Can view permission',8,'view_permission'),
(14,'Can add group',9,'add_group'),
(15,'Can change group',9,'change_group'),
(16,'Can delete group',9,'delete_group'),
(17,'Can view group',9,'view_group'),
(18,'Can add user',1,'add_user'),
(19,'Can change user',1,'change_user'),
(20,'Can delete user',1,'delete_user'),
(21,'Can view user',1,'view_user'),
(22,'Can add content type',10,'add_contenttype'),
(23,'Can change content type',10,'change_contenttype'),
(24,'Can delete content type',10,'delete_contenttype'),
(25,'Can view content type',10,'view_contenttype'),
(26,'Can add 系统公告表',11,'add_bnotice'),
(27,'Can change 系统公告表',11,'change_bnotice'),
(28,'Can delete 系统公告表',11,'delete_bnotice'),
(29,'Can view 系统公告表',11,'view_bnotice'),
(30,'Can add 商品分类表',12,'add_category'),
(31,'Can change 商品分类表',12,'change_category'),
(32,'Can delete 商品分类表',12,'delete_category'),
(33,'Can view 商品分类表',12,'view_category'),
(34,'Can add 用户信息表',13,'add_userinfo'),
(35,'Can change 用户信息表',13,'change_userinfo'),
(36,'Can delete 用户信息表',13,'delete_userinfo'),
(37,'Can view 用户信息表',13,'view_userinfo'),
(38,'Can add 商品表',14,'add_product'),
(39,'Can change 商品表',14,'change_product'),
(40,'Can delete 商品表',14,'delete_product'),
(41,'Can view 商品表',14,'view_product'),
(42,'Can add 商品图片表',15,'add_productimage'),
(43,'Can change 商品图片表',15,'change_productimage'),
(44,'Can delete 商品图片表',15,'delete_productimage'),
(45,'Can view 商品图片表',15,'view_productimage'),
(46,'Can add 用户浏览记录表',16,'add_record'),
(47,'Can change 用户浏览记录表',16,'change_record'),
(48,'Can delete 用户浏览记录表',16,'delete_record'),
(49,'Can view 用户浏览记录表',16,'view_record'),
(50,'Can add 用户购物车表',17,'add_cart'),
(51,'Can change 用户购物车表',17,'change_cart'),
(52,'Can delete 用户购物车表',17,'delete_cart'),
(53,'Can view 用户购物车表',17,'view_cart'),
(54,'Can add 用户操作日志表',18,'add_bop'),
(55,'Can change 用户操作日志表',18,'change_bop'),
(56,'Can delete 用户操作日志表',18,'delete_bop'),
(57,'Can view 用户操作日志表',18,'view_bop'),
(58,'Can add 用户登录日志表',19,'add_blogin'),
(59,'Can change 用户登录日志表',19,'change_blogin'),
(60,'Can delete 用户登录日志表',19,'delete_blogin'),
(61,'Can view 用户登录日志表',19,'view_blogin'),
(62,'Can add 系统错误日志表',20,'add_berror'),
(63,'Can change 系统错误日志表',20,'change_berror'),
(64,'Can delete 系统错误日志表',20,'delete_berror'),
(65,'Can view 系统错误日志表',20,'view_berror'),
(66,'Can add 用户地址表',21,'add_address'),
(67,'Can change 用户地址表',21,'change_address'),
(68,'Can delete 用户地址表',21,'delete_address'),
(69,'Can view 用户地址表',21,'view_address'),
(70,'Can add 订单表',22,'add_userorder'),
(71,'Can change 订单表',22,'change_userorder'),
(72,'Can delete 订单表',22,'delete_userorder'),
(73,'Can view 订单表',22,'view_userorder'),
(74,'Can add 线下交易预约表',23,'add_reserve'),
(75,'Can change 线下交易预约表',23,'change_reserve'),
(76,'Can delete 线下交易预约表',23,'delete_reserve'),
(77,'Can view 线下交易预约表',23,'view_reserve'),
(78,'Can add 交易评论表',24,'add_comment'),
(79,'Can change 交易评论表',24,'change_comment'),
(80,'Can delete 交易评论表',24,'delete_comment'),
(81,'Can view 交易评论表',24,'view_comment'),
(82,'Can add 用户收藏表',25,'add_favorite'),
(83,'Can change 用户收藏表',25,'change_favorite'),
(84,'Can delete 用户收藏表',25,'delete_favorite'),
(85,'Can view 用户收藏表',25,'view_favorite'),
(86,'Can add 轮播图表',26,'add_banner'),
(87,'Can change 轮播图表',26,'change_banner'),
(88,'Can delete 轮播图表',26,'delete_banner'),
(89,'Can view 轮播图表',26,'view_banner'),
(90,'Can add session',27,'add_session'),
(91,'Can change session',27,'change_session'),
(92,'Can delete session',27,'delete_session'),
(93,'Can view session',27,'view_session');
UNLOCK TABLES;

--
-- Dumping data for table `auth_user`
--
LOCK TABLES `auth_user` WRITE;
INSERT INTO `auth_user` VALUES 
(1,'pbkdf2_sha256$260000$...','2025-12-07 23:08:38.972202',1,'admin','Admin','User','admin@campus.edu',1,1,'2025-12-07 23:08:38.972202'),
(2,'pbkdf2_sha256$260000$...','2025-12-07 23:08:38.972202',0,'student1','Student','One','student1@campus.edu',0,1,'2025-12-07 23:08:38.972202');
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_groups`
--
LOCK TABLES `auth_user_groups` WRITE;
INSERT INTO `auth_user_groups` VALUES 
(1,1,1),
(2,2,2);
UNLOCK TABLES;

--
-- Dumping data for table `b_login`
--
LOCK TABLES `b_login` WRITE;
INSERT INTO `b_login` VALUES 
(1,'2025-12-08 12:38:12.940942','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',1,8),
(2,'2025-12-08 12:44:15.418025','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',1,1),
(3,'2025-12-08 17:51:11.785362','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',1,8),
(4,'2025-12-08 20:28:37.695057','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',1,8),
(5,'2025-12-09 16:00:13.388939','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',1,1),
(6,'2025-12-10 21:21:03.394151','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',1,1);
UNLOCK TABLES;

--
-- Dumping data for table `b_notice`
--
LOCK TABLES `b_notice` WRITE;
INSERT INTO `b_notice` VALUES 
(1,'【重要】平台实名认证已开启，请尽快绑定学号！','2025-12-07 23:08:39.024976',1),
(2,'禁止发布食品、药品及违禁物品，违者永久封号。','2025-12-07 23:08:39.024976',2),
(3,'客服邮箱：1575100890@qq.com（工作日 9:00-17:00）','2025-12-07 23:08:39.024976',3),
(4,'123456','2025-12-08 21:09:10.590498',13);
UNLOCK TABLES;

--
-- Dumping data for table `cart`
--
LOCK TABLES `cart` WRITE;
INSERT INTO `cart` VALUES 
(1,'2025-12-07 23:08:39.033592',2,3);
UNLOCK TABLES;

--
-- Dumping data for table `category`
--
LOCK TABLES `category` WRITE;
INSERT INTO `category` VALUES 
(1,'数码电子',1,'2025-12-07 23:08:38.955054'),
(2,'图书教材',2,'2025-12-07 23:08:38.955054'),
(3,'服饰鞋包',3,'2025-12-07 23:08:38.955054'),
(4,'运动户外',4,'2025-12-07 23:08:38.955054'),
(7,'test345',0,'2025-12-08 12:53:20.774506'),
(8,'test2',0,'2025-12-08 21:05:37.333443');
UNLOCK TABLES;

--
-- Dumping data for table `comment`
--
LOCK TABLES `comment` WRITE;
INSERT INTO `comment` VALUES 
(1,'这是一条模拟评论',8,0,'2025-12-08 21:21:39.210640',8,10,NULL,'2025-12-08 21:21:39.210640',0,13),
(2,'这是一条模拟评论',8,0,'2025-12-08 21:21:42.998689',8,10,NULL,'2025-12-08 21:21:42.998689',0,13),
(3,'这是一条模拟评论',8,0,'2025-12-08 21:35:52.378719',8,10,NULL,'2025-12-08 21:35:52.378719',0,13),
(5,'test',5,0,'2025-12-08 21:47:34.392636',3,2,NULL,'2025-12-08 21:47:34.392636',0,2),
(6,'test',6,0,'2025-12-08 21:47:41.797697',3,2,NULL,'2025-12-08 21:47:41.797697',0,2),
(7,'test',10,0,'2025-12-09 11:57:08.904914',4,8,NULL,'2025-12-09 11:57:08.904914',0,4),
(8,'这是第二条评论',10,0,'2025-12-09 11:57:20.254585',4,8,NULL,'2025-12-09 11:57:20.254585',0,4),
(9,'这是第一条评论',10,0,'2025-12-09 11:57:31.962785',1,8,NULL,'2025-12-09 11:57:31.962785',0,3),
(10,'test内容',10,0,'2025-12-10 12:39:46.916000',3,2,NULL,'2025-12-10 12:39:46.916000',0,2);
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--
LOCK TABLES `django_admin_log` WRITE;
-- （通常开发环境可为空，此处省略示例数据）
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--
LOCK TABLES `django_content_type` WRITE;
INSERT INTO `django_content_type` VALUES 
(1,'auth','user','用户'),
(2,'myapp','product','商品'),
(3,'admin','logentry','日志条目'),
(4,'myapp','userorder','订单'),
(7,'admin','logentry','日志条目'),
(8,'auth','permission','权限'),
(9,'auth','group','组'),
(10,'contenttypes','contenttype','内容类型'),
(11,'myapp','bnotice','系统公告表'),
(12,'myapp','category','商品分类表'),
(13,'myapp','userinfo','用户信息表'),
(14,'myapp','product','商品表'),
(15,'myapp','productimage','商品图片表'),
(16,'myapp','record','用户浏览记录表'),
(17,'myapp','cart','用户购物车表'),
(18,'myapp','bop','用户操作日志表'),
(19,'myapp','blogin','用户登录日志表'),
(20,'myapp','berror','系统错误日志表'),
(21,'myapp','address','用户地址表'),
(22,'myapp','userorder','订单表'),
(23,'myapp','reserve','线下交易预约表'),
(24,'myapp','comment','交易评论表'),
(25,'myapp','favorite','用户收藏表'),
(26,'myapp','banner','轮播图表'),
(27,'sessions','session','会话');
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--
LOCK TABLES `django_migrations` WRITE;
-- （建议由 Django 自动管理，可不插入）
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--
LOCK TABLES `django_session` WRITE;
-- （会话数据动态生成，通常不预置）
UNLOCK TABLES;

--
-- Dumping data for table `favorite`
--
LOCK TABLES `favorite` WRITE;
INSERT INTO `favorite` VALUES 
(1,'2025-12-07 23:08:39.033592',2,3);
UNLOCK TABLES;

--
-- Dumping data for table `product`
--
-- 注意：已移除 wish_count 字段！字段顺序需与 create_tables.sql 一致
LOCK TABLES `product` WRITE;
INSERT INTO `product` (
    `product_id`, `product_title`, `product_o_price`, `product_price`, 
    `product_status`, `quality`, `reject_reason`, `create_time`, 
    `update_time`, `content`, `view_count`, `collect_count`, 
    `category`, `user_id`, `is_reserved`, `cover_image_id`, `location`
) VALUES 
(1,'二手 iPhone 13',3000,2500,1,9,'', '2025-12-07 23:08:38.955054', '2025-12-07 23:08:38.955054', '几乎全新，原装充电器',10,5,1,2,0,NULL,'信息中心'),
(2,'高等数学（第七版）',50,30,1,8,NULL,'2025-12-07 23:08:38.955054','2025-12-07 23:08:38.955054','教材，有笔记',20,3,2,3,0,NULL,'计算机学院'),
(3,'MacBook Pro 2020',8000,6500,1,9,NULL,'2025-12-07 23:08:38.955054','2025-12-07 23:08:38.955054','M1芯片，16G内存',15,2,1,4,0,NULL,'电子工程学院'),
(4,'耐克运动鞋',600,400,1,7,NULL,'2025-12-07 23:08:38.955054','2025-12-07 23:08:38.955054','穿了几次，9成新',8,1,3,5,0,NULL,'文学院'),
(13,'测试商品',100,80,1,10,NULL,'2025-12-08 21:15:10.000000','2025-12-08 21:15:10.000000','',0,0,1,8,0,NULL,NULL);
UNLOCK TABLES;

--
-- Dumping data for table `product_image`
--
LOCK TABLES `product_image` WRITE;
INSERT INTO `product_image` VALUES 
(1,'/media/product/iphone13_1.jpg',1,1),
(2,'/media/product/math_book.jpg',1,2),
(3,'/media/product/macbook.jpg',1,3),
(4,'/media/product/nike_shoes.jpg',1,4),
(13,'/media/product/test.jpg',1,13);
UNLOCK TABLES;

--
-- Dumping data for table `record`
--
LOCK TABLES `record` WRITE;
INSERT INTO `record` VALUES 
(1,'2025-12-07 23:08:39.033592',2,3);
UNLOCK TABLES;

--
-- Dumping data for table `reserve`
--
LOCK TABLES `reserve` WRITE;
INSERT INTO `reserve` VALUES 
(1,1,'2025-12-08 21:30:00.000000',NULL,NULL,3,2,NULL,2,NULL,NULL,NULL),
(2,2,'2025-12-09 12:00:00.000000','2025-12-09 12:30:00.000000',4,4,8,NULL,4,'按时交易','2025-12-09 12:00:00.000000','图书馆前');
UNLOCK TABLES;

--
-- Dumping data for table `user_info`
--
LOCK TABLES `user_info` WRITE;
INSERT INTO `user_info` VALUES 
(1,'20210001','hashed_password','系统管理员','信息学院','admin@campus.edu','13800000001','2025-12-07 23:08:38.955054',1,'/media/avatar/admin.png',NULL,'A'),
(2,'20210002','hashed_password','张三','计算机学院','zhangsan@campus.edu','13800000002','2025-12-07 23:08:38.955054',1,'/media/avatar/zs.png',NULL,'S'),
(3,'20210003','hashed_password','李四','电子工程学院','lisi@campus.edu','13800000003','2025-12-07 23:08:38.955054',1,'/media/avatar/ls.png',NULL,'S'),
(4,'20210004','hashed_password','王五','文学院','wangwu@campus.edu','13800000004','2025-12-07 23:08:38.955054',1,'/media/avatar/ww.png',NULL,'S'),
(5,'20210005','hashed_password','赵六','经管学院','zhaoliu@campus.edu','13800000005','2025-12-07 23:08:38.955054',1,'/media/avatar/zl.png',NULL,'S'),
(6,'20210006','hashed_password','小美','艺术学院','xiaomei@campus.edu','13800000006','2025-12-07 23:08:38.955054',1,'/media/avatar/xm.png',NULL,'S'),
(8,'20210008','hashed_password','林志宇','计算机学院','linzhiyu@example.com','15305977276','2025-12-08 12:38:12.940942',1,'/media/avatar/default.png',NULL,'S');
UNLOCK TABLES;

--
-- Dumping data for table `user_order`
--
LOCK TABLES `user_order` WRITE;
INSERT INTO `user_order` VALUES 
(1,'高等数学（第七版）','/media/product/math_book.jpg',30.00,1,'2025-12-08 21:30:00.000000',NULL,NULL,NULL,NULL,2,3,2);
UNLOCK TABLES;