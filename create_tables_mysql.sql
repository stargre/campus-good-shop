-- MySQL dump (cleaned: only business tables for campus_shop)

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user_info`
--
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_collage` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_mobile` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_create_time` datetime(6) NOT NULL,
  `user_status` int NOT NULL,
  `user_avart` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_student_id` (`user_student_id`),
  UNIQUE KEY `user_email` (`user_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `address`
--
DROP TABLE IF EXISTS `address`;
CREATE TABLE `address` (
  `address_id` int NOT NULL AUTO_INCREMENT,
  `receiver_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiver_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiver_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_default` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`address_id`),
  KEY `address_user_id_c030de7d_fk_user_info_user_id` (`user_id`),
  CONSTRAINT `address_user_id_c030de7d_fk_user_info_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `category`
--
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category_sort_order` int NOT NULL,
  `category_create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `product`
--
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `product_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_o_price` int NOT NULL,
  `product_price` int NOT NULL,
  `product_status` int NOT NULL,
  `quality` int NOT NULL,
  `reject_reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `view_count` int NOT NULL,
  `collect_count` int NOT NULL,
  `category` int NOT NULL,
  `user_id` int NOT NULL,
  `is_reserved` tinyint(1) NOT NULL,
  `cover_image_id` int DEFAULT NULL,
  `location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`product_id`),
  KEY `product_category_574553b9_fk_category_category_id` (`category`),
  KEY `product_user_id_091f6d86_fk_user_info_user_id` (`user_id`),
  CONSTRAINT `product_category_574553b9_fk_category_category_id` FOREIGN KEY (`category`) REFERENCES `category` (`category_id`),
  CONSTRAINT `product_user_id_091f6d86_fk_user_info_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `product_image`
--
DROP TABLE IF EXISTS `product_image`;
CREATE TABLE `product_image` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL,
  `product_id` int NOT NULL,
  PRIMARY KEY (`image_id`),
  KEY `product_image_product_id_8b9355c5_fk_product_product_id` (`product_id`),
  CONSTRAINT `product_image_product_id_8b9355c5_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `favorite`
--
DROP TABLE IF EXISTS `favorite`;
CREATE TABLE `favorite` (
  `favorite_id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `product_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`favorite_id`),
  UNIQUE KEY `favorite_user_id_product_id_80d57210_uniq` (`user_id`,`product_id`),
  KEY `favorite_product_id_f7399ea1_fk_product_product_id` (`product_id`),
  CONSTRAINT `favorite_product_id_f7399ea1_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `favorite_user_id_8a5f8d2c_fk_user_info_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `record`
--
DROP TABLE IF EXISTS `record`;
CREATE TABLE `record` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `product_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`record_id`),
  KEY `record_product_id_18d0ca92_fk_product_product_id` (`product_id`),
  KEY `record_user_id_892e847f_fk_user_info_user_id` (`user_id`),
  CONSTRAINT `record_product_id_18d0ca92_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `record_user_id_892e847f_fk_user_info_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `comment`
--
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `comment_content` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rating` int NOT NULL,
  `comment_status` int NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `seller_id` int NOT NULL,
  `user_id` int NOT NULL,
  `order_id` int DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `like_count` int NOT NULL,
  `product_id` int DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `comment_seller_id_cf712d43_fk_user_info_user_id` (`seller_id`),
  KEY `comment_user_id_2224f9d1_fk_user_info_user_id` (`user_id`),
  KEY `comment_product_id_62c0c379_fk_product_product_id` (`product_id`),
  KEY `comment_order_id_c2e30380_fk_user_order_order_id` (`order_id`),
  CONSTRAINT `comment_order_id_c2e30380_fk_user_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `user_order` (`order_id`),
  CONSTRAINT `comment_product_id_62c0c379_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `comment_seller_id_cf712d43_fk_user_info_user_id` FOREIGN KEY (`seller_id`) REFERENCES `user_info` (`user_id`),
  CONSTRAINT `comment_user_id_2224f9d1_fk_user_info_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Table structure for table `user_order`
--
DROP TABLE IF EXISTS `user_order`;
CREATE TABLE `user_order` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `product_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `order_status` int NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `pay_time` datetime(6) DEFAULT NULL,
  `receive_time` datetime(6) DEFAULT NULL,
  `cancel_time` datetime(6) DEFAULT NULL,
  `refund_reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `product_id` int NOT NULL,
  `seller_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `user_order_product_id_5bea5130_fk_product_product_id` (`product_id`),
  KEY `user_order_seller_id_85e5d92a_fk_user_info_user_id` (`seller_id`),
  KEY `user_order_user_id_1247599d_fk_user_info_user_id` (`user_id`),
  CONSTRAINT `user_order_product_id_5bea5130_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `user_order_seller_id_85e5d92a_fk_user_info_user_id` FOREIGN KEY (`seller_id`) REFERENCES `user_info` (`user_id`),
  CONSTRAINT `user_order_user_id_1247599d_fk_user_info_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `b_notice`
--
DROP TABLE IF EXISTS `b_notice`;
CREATE TABLE `b_notice` (
  `b_notice_id` int NOT NULL AUTO_INCREMENT,
  `notice_content` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `sort_value` int NOT NULL,
  PRIMARY KEY (`b_notice_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


--
-- Table structure for table `password_reset`
--
DROP TABLE IF EXISTS `password_reset`;
CREATE TABLE `password_reset` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expire_at` datetime(6) DEFAULT NULL,
  `used` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  `code` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `password_reset_user_id_d6a4e93d_fk_user_info_user_id` (`user_id`),
  CONSTRAINT `password_reset_user_id_d6a4e93d_fk_user_info_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;