"""
数据模型定义模块
定义了校园二手交易平台的所有数据模型类
"""
from django.db import models
import datetime

# 用户信息表
class UserInfo(models.Model):
    """
    用户信息模型
    用于存储平台所有用户的基本信息
    """
    user_id = models.AutoField(primary_key=True)
    user_student_id = models.CharField(max_length=20, verbose_name='学号', unique=True)
    user_password = models.CharField(max_length=50, verbose_name='密码')
    user_name = models.CharField(max_length=20, verbose_name='用户真实姓名')
    user_collage = models.CharField(max_length=20, verbose_name='用户所在学院', null=True, blank=True)
    user_email = models.CharField(max_length=100, verbose_name='用户邮箱', unique=True)
    user_create_time = models.DateTimeField(verbose_name='用户注册时间', default=datetime.datetime.now)
    user_status = models.IntegerField(verbose_name='用户状态', choices=((0, '禁用'), (1, '正常')), default=1)
    user_avart = models.CharField(max_length=255, verbose_name='用户头像路径', default='default-avatar.jpg')
    token = models.CharField(max_length=100, verbose_name='token', null=True, blank=True)  # 为了保持与现有认证系统兼容
    
    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息表'
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
    user_id = models.ForeignKey(UserInfo, verbose_name='发布者用户ID', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='商品分类ID', on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255, verbose_name='商品标题')
    product_o_price = models.IntegerField(verbose_name='商品原价（单位：分）')
    product_price = models.IntegerField(verbose_name='商品现价（单位：分）')
    product_status = models.IntegerField(verbose_name='商品状态', choices=((0, '待审核'), (1, '审核通过'), (2, '审核不通过'), (3, '已售出')), default=0)
    quality = models.IntegerField(verbose_name='商品成色', choices=((1, '全新'), (2, '几乎全新'), (3, '轻微使用痕迹'), (4, '明显使用痕迹')), default=1)
    reject_reason = models.CharField(max_length=255, verbose_name='审核不通过原因', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='商品创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='商品最后更新时间', auto_now=True)
    content = models.TextField(verbose_name='商品描述', null=True, blank=True)  # 为了保持与现有系统兼容
    view_count = models.IntegerField(verbose_name='浏览次数', default=0)  # 为了保持与现有系统兼容
    wish_count = models.IntegerField(verbose_name='心愿次数', default=0)  # 为了保持与现有系统兼容
    collect_count = models.IntegerField(verbose_name='收藏次数', default=0)  # 为了保持与现有系统兼容
    
    class Meta:
        db_table = 'product'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name

# 标签表
class Tag(models.Model):
    """
    标签模型
    用于商品标签管理
    """
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=50, verbose_name='标签名称', unique=True)
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    
    class Meta:
        db_table = 'tag'
        verbose_name = '商品标签表'
        verbose_name_plural = verbose_name

# 商品-标签关联表
class ProductTag(models.Model):
    """
    商品标签关联模型
    用于存储商品和标签的多对多关系
    """
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, verbose_name='商品ID', on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, verbose_name='标签ID', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_tag'
        verbose_name = '商品标签关联表'
        verbose_name_plural = verbose_name

# 为Product模型添加tags字段
Product.add_to_class('tags', models.ManyToManyField(Tag, through='ProductTag', verbose_name='商品标签', related_name='products'))

# 商品图片表
class ProductImage(models.Model):
    """
    商品图片模型
    用于存储商品的图片信息
    """
    image_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, verbose_name='关联的商品ID', on_delete=models.CASCADE)
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
    user_id = models.ForeignKey(UserInfo, verbose_name='关联的用户ID', on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=50, verbose_name='收货人姓名')
    receiver_phone = models.CharField(max_length=20, verbose_name='收货人电话')
    receiver_address = models.CharField(max_length=255, verbose_name='详细收货地址')
    is_default = models.IntegerField(verbose_name='是否默认地址', choices=((0, '否'), (1, '是')), default=0)
    
    class Meta:
        db_table = 'address'
        verbose_name = '用户地址表'
        verbose_name_plural = verbose_name

# 购物车表
class Cart(models.Model):
    """
    购物车模型
    用于存储用户的购物车信息
    """
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='关联的用户ID', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, verbose_name='关联的商品ID', on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='加入购物车时间', default=datetime.datetime.now)
    
    class Meta:
        db_table = 'cart'
        verbose_name = '用户购物车表'
        verbose_name_plural = verbose_name

# 订单表
class UserOrder(models.Model):
    """
    订单模型
    用于存储交易订单信息
    """
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='买家用户ID', on_delete=models.CASCADE, related_name='buyer_orders')
    seller_id = models.ForeignKey(UserInfo, verbose_name='卖家用户ID', on_delete=models.CASCADE, related_name='seller_orders')
    product_id = models.ForeignKey(Product, verbose_name='关联的商品ID', on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255, verbose_name='商品标题（下单时的快照）')
    product_image = models.CharField(max_length=255, verbose_name='商品主图（下单时的快照）')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成交价格')
    order_status = models.IntegerField(verbose_name='订单状态', choices=((0, '待支付'), (1, '已支付'), (2, '已发货'), (3, '已完成'), (4, '已取消'), (5, '退款中')))
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
    order_id = models.ForeignKey(UserOrder, verbose_name='关联的订单ID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserInfo, verbose_name='评论用户ID（买家）', on_delete=models.CASCADE, related_name='comments_as_user')
    seller_id = models.ForeignKey(UserInfo, verbose_name='被评论的卖家ID', on_delete=models.CASCADE, related_name='comments_as_seller') 
    comment_content = models.CharField(max_length=1000, verbose_name='评论内容', null=True, blank=True)
    rating = models.IntegerField(verbose_name='评分：1-10分', default=10)
    comment_status = models.IntegerField(verbose_name='评论状态', choices=((0, '正常'), (1, '隐藏')), default=0)
    create_time = models.DateTimeField(verbose_name='评论时间', default=datetime.datetime.now)
    
    class Meta:
        db_table = 'comment'
        verbose_name = '交易评论表'
        verbose_name_plural = verbose_name

# 预约表
class Reserve(models.Model):
    """
    预约模型
    用于线下交易预约信息
    """
    reserve_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(UserOrder, verbose_name='关联的订单ID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserInfo, verbose_name='预约用户ID（买家）', on_delete=models.CASCADE,  related_name='reserves_as_user')
    seller_id = models.ForeignKey(UserInfo, verbose_name='卖家用户ID', on_delete=models.CASCADE, related_name='reserves_as_seller')
    address_id = models.ForeignKey(Address, verbose_name='交易地址ID', on_delete=models.CASCADE)
    reserve_status = models.IntegerField(verbose_name='预约状态', choices=((0, '待确认'), (1, '已确认'), (2, '已完成'), (3, '已取消')), default=0)
    create_time = models.DateTimeField(verbose_name='预约创建时间', default=datetime.datetime.now)
    finish_time = models.DateTimeField(verbose_name='预约完成时间', null=True, blank=True)
    
    class Meta:
        db_table = 'reserve'
        verbose_name = '线下交易预约表'
        verbose_name_plural = verbose_name

# 浏览记录表
class Record(models.Model):
    """
    浏览记录模型
    用于存储用户的商品浏览历史
    """
    record_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='用户ID', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, verbose_name='商品ID', on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='浏览时间', default=datetime.datetime.now)
    
    class Meta:
        db_table = 'record'
        verbose_name = '用户浏览记录表'
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

# 登录日志表
class BLogin(models.Model):
    """
    登录日志模型
    用于存储用户登录日志
    """
    b_login_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='用户ID', on_delete=models.CASCADE)
    login_time = models.DateTimeField(verbose_name='登录时间', default=datetime.datetime.now)
    ip_address = models.CharField(max_length=50, verbose_name='登录IP地址', null=True, blank=True)
    login_device = models.CharField(max_length=100, verbose_name='登录设备信息', null=True, blank=True)
    login_status = models.BooleanField(verbose_name='登录是否成功', null=True, blank=True)
    
    class Meta:
        db_table = 'b_login'
        verbose_name = '用户登录日志表'
        verbose_name_plural = verbose_name

# 操作日志表
class BOp(models.Model):
    """
    操作日志模型
    用于存储用户操作日志
    """
    b_op_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='用户ID', on_delete=models.CASCADE)
    op_time = models.DateTimeField(verbose_name='操作时间', default=datetime.datetime.now)
    op_type = models.CharField(max_length=20, verbose_name='操作类型', null=True, blank=True)
    op_object = models.CharField(max_length=100, verbose_name='操作对象', null=True, blank=True)
    op_detail = models.TextField(verbose_name='操作详情', null=True, blank=True)
    
    class Meta:
        db_table = 'b_op'
        verbose_name = '用户操作日志表'
        verbose_name_plural = verbose_name

# 错误日志表
class BError(models.Model):
    """
    错误日志模型
    用于存储系统错误日志
    """
    b_error_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, verbose_name='用户ID（触发错误的用户）', on_delete=models.CASCADE)
    error_type = models.CharField(max_length=50, verbose_name='错误类型')
    error_code = models.IntegerField(verbose_name='错误代码')
    error_time = models.DateTimeField(verbose_name='错误发生时间', default=datetime.datetime.now)
    error_message = models.TextField(verbose_name='错误信息')
    handle_status = models.CharField(max_length=20, verbose_name='处理状态', default='未处理')
    handle_time = models.DateTimeField(verbose_name='处理时间', null=True, blank=True)
    handle_detail = models.TextField(verbose_name='处理详情', null=True, blank=True)
    
    class Meta:
        db_table = 'b_error'
        verbose_name = '系统错误日志表'
        verbose_name_plural = verbose_name
