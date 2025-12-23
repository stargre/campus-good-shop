"""
数据模型定义模块
定义了校园二手交易平台的所有数据模型类
"""
from django.db import models
import datetime

# 用户信息表
class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_student_id = models.CharField(max_length=20, verbose_name='学号', unique=True)
    user_password = models.CharField(max_length=50, verbose_name='密码')
    user_name = models.CharField(max_length=20, verbose_name='用户真实姓名')
    user_collage = models.CharField(max_length=20, verbose_name='用户所在学院', null=True, blank=True)
    user_email = models.CharField(max_length=100, verbose_name='用户邮箱', unique=True)
    user_mobile = models.CharField(max_length=20, verbose_name='用户手机号', null=True, blank=True)
    user_create_time = models.DateTimeField(verbose_name='用户注册时间', default=datetime.datetime.now)
    user_status = models.IntegerField(verbose_name='用户状态', choices=((0, '禁用'), (1, '正常')), default=1)
    user_avart = models.CharField(max_length=255, verbose_name='用户头像路径', default='default-avatar.jpg')
    token = models.CharField(max_length=100, verbose_name='token', null=True, blank=True)
    
    # 修改role字段的选项，添加超级管理员角色
    role = models.CharField(
        max_length=1, 
        verbose_name='用户角色', 
        choices=(
            ('0', '超级管理员'),  # 添加超级管理员
            ('1', '普通管理员'), 
            ('2', '普通用户'), 
            ('3', '演示账号')
        ), 
        default='2'  # 默认普通用户
    )

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name


# 密码找回表（存放重置令牌）
class PasswordReset(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, verbose_name='关联用户', on_delete=models.CASCADE, db_column='user_id')
    token = models.CharField(max_length=128, verbose_name='重置令牌', unique=True)
    code = models.CharField(max_length=10, verbose_name='验证码', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    expire_at = models.DateTimeField(verbose_name='过期时间', null=True, blank=True)
    used = models.BooleanField(verbose_name='是否已使用', default=False)

    class Meta:
        db_table = 'password_reset'
        verbose_name = '密码找回令牌表'
        verbose_name_plural = verbose_name

# 商品分类表
class Category(models.Model):
    """
    分类模型
    用于商品分类管理
    """
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, verbose_name='分类名称', unique=True)
    category_sort_order = models.IntegerField(verbose_name='分类排序值', default=0)
    category_create_time = models.DateTimeField(verbose_name='分类创建时间', default=datetime.datetime.now)
    
    class Meta:
        db_table = 'category'
        verbose_name = '商品分类表'
        verbose_name_plural = verbose_name

# 商品表
class Product(models.Model):
    """
    商品模型
    用于存储所有发布的商品信息
    """
    product_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='发布者用户ID', on_delete=models.CASCADE, db_column='user_id')
    category = models.ForeignKey(Category, verbose_name='商品分类ID', on_delete=models.CASCADE, db_column='category')
    product_title = models.CharField(max_length=255, verbose_name='商品标题')
    product_o_price = models.IntegerField(verbose_name='商品原价（单位：分）')
    product_price = models.IntegerField(verbose_name='商品现价（单位：分）')
    product_status = models.IntegerField(verbose_name='商品状态', choices=((0, '待审核'), (1, '审核通过'), (2, '审核不通过'), (3, '已售出')), default=0)
    quality = models.IntegerField(verbose_name='商品成色', choices=((1, '全新'), (2, '几乎全新'), (3, '轻微使用痕迹'), (4, '明显使用痕迹')), default=1)
    create_time = models.DateTimeField(verbose_name='商品创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='商品最后更新时间', auto_now=True)
    content = models.TextField(verbose_name='商品描述', null=True, blank=True)
    # 交易地点（新增）
    location = models.CharField(max_length=255, verbose_name='交易地点', null=True, blank=True)
    is_reserved = models.BooleanField(verbose_name='是否已预约', default=False)
    cover_image_id = models.IntegerField(verbose_name='主图ID', null=True, blank=True)
    
    class Meta:
        db_table = 'product'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name



# 商品图片表
class ProductImage(models.Model):
    """
    商品图片模型
    用于存储商品的图片信息
    """
    image_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, verbose_name='关联的商品ID', on_delete=models.CASCADE, db_column='product_id')
    image_url = models.CharField(max_length=255, verbose_name='图片URL路径')
    sort_order = models.IntegerField(verbose_name='图片排序', default=0)
    
    class Meta:
        db_table = 'product_image'
        verbose_name = '商品图片表'
        verbose_name_plural = verbose_name

# 地址表
class Address(models.Model):
    """
    地址模型
    用于存储用户的收货地址信息
    """
    address_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='关联的用户ID', on_delete=models.CASCADE, db_column='user_id')
    receiver_name = models.CharField(max_length=50, verbose_name='收货人姓名')
    receiver_phone = models.CharField(max_length=20, verbose_name='收货人电话')
    receiver_address = models.CharField(max_length=255, verbose_name='详细收货地址')
    is_default = models.IntegerField(verbose_name='是否默认地址', choices=((0, '否'), (1, '是')), default=0)
    
    class Meta:
        db_table = 'address'
        verbose_name = '用户地址表'
        verbose_name_plural = verbose_name


# 订单表
class UserOrder(models.Model):
    """
    订单模型
    用于存储交易订单信息
    """
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='买家用户ID', on_delete=models.CASCADE, related_name='buyer_orders', db_column='user_id')
    seller_id = models.ForeignKey(UserInfo, verbose_name='卖家用户ID', on_delete=models.CASCADE, related_name='seller_orders', db_column='seller_id')
    product_id = models.ForeignKey(Product, verbose_name='关联的商品ID', on_delete=models.CASCADE, db_column='product_id')
    product_title = models.CharField(max_length=255, verbose_name='商品标题（下单时的快照）')
    product_image = models.CharField(max_length=255, verbose_name='商品主图（下单时的快照）',blank=True,default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成交价格')
    order_status = models.IntegerField(verbose_name='订单状态', choices=((0, '待支付'), (1, '已支付'), (2, '已发货'), (3, '已完成'), (4, '已取消'), (5, '已退款')))
    create_time = models.DateTimeField(verbose_name='订单创建时间', default=datetime.datetime.now)
    pay_time = models.DateTimeField(verbose_name='支付时间', null=True, blank=True)
    receive_time = models.DateTimeField(verbose_name='收货时间', null=True, blank=True)
    cancel_time = models.DateTimeField(verbose_name='取消时间', null=True, blank=True)
    refund_reason = models.CharField(max_length=255, verbose_name='退款原因', null=True, blank=True)
    
    class Meta:
        db_table = 'user_order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name

# 评论表
class Comment(models.Model):
    """
    评论模型
    用于存储用户对交易的评价信息
    """
    comment_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, verbose_name='关联的商品ID', on_delete=models.CASCADE, db_column='product_id', null=True, blank=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='评论用户ID（买家）', on_delete=models.CASCADE, related_name='comments_as_user', db_column='user_id')
    seller_id = models.ForeignKey(UserInfo, verbose_name='被评论的卖家ID', on_delete=models.CASCADE, related_name='comments_as_seller', db_column='seller_id')
    comment_content = models.CharField(max_length=1000, verbose_name='评论内容', null=True, blank=True)
    rating = models.IntegerField(verbose_name='评分：1-10分', default=10)
    comment_status = models.IntegerField(verbose_name='评论状态', choices=((0, '正常'), (1, '隐藏')), default=0)
    create_time = models.DateTimeField(verbose_name='评论时间', default=datetime.datetime.now)
    
    class Meta:
        db_table = 'comment'
        verbose_name = '交易评论表'
        verbose_name_plural = verbose_name


# 公告表
class BNotice(models.Model):
    """
    公告模型
    用于系统公告信息
    """
    b_notice_id = models.AutoField(primary_key=True)
    notice_content = models.CharField(max_length=1000, verbose_name='公告内容')
    create_time = models.DateTimeField(verbose_name='公告发布时间', default=datetime.datetime.now)
    sort_value = models.IntegerField(verbose_name='公告排序', default=0)
    
    class Meta:
        db_table = 'b_notice'
        verbose_name = '系统公告表'
        verbose_name_plural = verbose_name



# 收藏表
class Favorite(models.Model):
    """
    收藏模型
    用于存储用户的商品收藏信息
    """
    favorite_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='用户ID', on_delete=models.CASCADE, db_column='user_id')
    product_id = models.ForeignKey(Product, verbose_name='商品ID', on_delete=models.CASCADE, db_column='product_id')
    create_time = models.DateTimeField(verbose_name='收藏时间', default=datetime.datetime.now)
    
    class Meta:
        db_table = 'favorite'
        verbose_name = '用户收藏表'
        verbose_name_plural = verbose_name
        # 确保用户不能重复收藏同一商品
        unique_together = ('user_id', 'product_id')

