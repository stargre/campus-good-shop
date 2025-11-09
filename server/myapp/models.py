"""
数据模型定义模块
定义了系统中的所有数据模型类，包括用户、商品、订单、评论等
"""
from django.db import models


class User(models.Model):
    """
    用户模型
    用于存储系统用户信息，包括管理员和普通用户
    """
    # 性别选择项
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    # 角色选择项：0-管理员，1-普通用户，2-前台用户，3-演示账号
    ROLE_CHOICES = (
        ('0', '管理员'),
        ('1', '普通用户'),
    )
    # 状态选择项：0-正常，1-封号
    STATUS_CHOICES = (
        ('0', '正常'),
        ('1', '封号'),
    )
    id = models.BigAutoField(primary_key=True)  # 主键ID
    username = models.CharField(max_length=50, null=True)  # 用户名
    password = models.CharField(max_length=50, null=True)  # 密码（MD5加密）
    role = models.CharField(max_length=2, blank=True, null=True)  # 角色：0-管理员，1-普通用户，2-前台用户
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')  # 账号状态
    nickname = models.CharField(blank=True, null=True, max_length=20)  # 昵称
    avatar = models.FileField(upload_to='avatar/', null=True)  # 头像文件路径
    mobile = models.CharField(max_length=13, blank=True, null=True)  # 手机号
    email = models.CharField(max_length=50, blank=True, null=True)  # 邮箱
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  # 性别
    description = models.TextField(max_length=200, null=True)  # 个人简介
    create_time = models.DateTimeField(auto_now_add=True, null=True)  # 创建时间
    score = models.IntegerField(default=0, blank=True, null=True)  # 积分
    push_email = models.CharField(max_length=40, blank=True, null=True)  # 推送邮箱
    push_switch = models.BooleanField(blank=True, null=True, default=False)  # 推送开关
    admin_token = models.CharField(max_length=32, blank=True, null=True)  # 后台管理Token
    token = models.CharField(max_length=32, blank=True, null=True)  # 前台用户Token

    class Meta:
        db_table = "b_user"  # 数据库表名


class Tag(models.Model):
    """
    标签模型
    用于商品标签分类
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    title = models.CharField(max_length=100, blank=True, null=True)  # 标签名称
    create_time = models.DateTimeField(auto_now_add=True, null=True)  # 创建时间

    class Meta:
        db_table = "b_tag"  # 数据库表名


class Classification(models.Model):
    """
    分类模型
    用于商品分类管理
    """
    list_display = ("title", "id")
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "b_classification"


class Thing(models.Model):
    """
    商品模型
    用于存储商品信息，包括商品详情、价格、库存等
    """
    # 商品状态：0-上架，1-下架
    STATUS_CHOICES = (
        ('0', '上架'),
        ('1', '下架'),
    )
    id = models.BigAutoField(primary_key=True)  # 主键ID
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='classification_thing')  # 分类外键
    tag = models.ManyToManyField(Tag, blank=True)  # 标签多对多关系
    title = models.CharField(max_length=100, blank=True, null=True)  # 商品标题
    cover = models.ImageField(upload_to='cover/', null=True)  # 商品封面图片
    description = models.TextField(max_length=1000, blank=True, null=True)  # 商品描述
    price = models.CharField(max_length=50, blank=True, null=True)  # 商品价格
    address = models.CharField(max_length=100, blank=True, null=True)  # 商品地址
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')  # 商品状态
    repertory = models.IntegerField(default=0)  # 库存数量
    score = models.IntegerField(default=0)  # 商品评分
    create_time = models.DateTimeField(auto_now_add=True, null=True)  # 创建时间
    pv = models.IntegerField(default=0)  # 浏览量
    recommend_count = models.IntegerField(default=0)  # 推荐次数
    wish = models.ManyToManyField(User, blank=True, related_name="wish_things")  # 心愿单用户多对多关系
    wish_count = models.IntegerField(default=0)  # 心愿单数量
    collect = models.ManyToManyField(User, blank=True, related_name="collect_things")  # 收藏用户多对多关系
    collect_count = models.IntegerField(default=0)  # 收藏数量

    class Meta:
            db_table = "b_thing"  # 数据库表名


class Comment(models.Model):
    """
    评论模型
    用于存储用户对商品的评论信息
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    content = models.CharField(max_length=200, blank=True, null=True)  # 评论内容
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_comment')  # 用户外键
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, null=True, related_name='thing_comment')  # 商品外键
    comment_time = models.DateTimeField(auto_now_add=True, null=True)  # 评论时间
    like_count = models.IntegerField(default=0)  # 点赞数量

    class Meta:
        db_table = "b_comment"


class Record(models.Model):
    """
    浏览记录模型
    用于记录用户浏览商品的历史记录
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_record')  # 用户外键
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, null=True, related_name='thing_record')  # 商品外键
    title = models.CharField(max_length=100, blank=True, null=True)  # 记录标题
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True,
                                       related_name='classification')  # 分类外键
    record_time = models.DateTimeField(auto_now_add=True, null=True)  # 记录时间

    class Meta:
        db_table = "b_record"  # 数据库表名


class LoginLog(models.Model):
    """
    登录日志模型
    用于记录用户登录的日志信息
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    username = models.CharField(max_length=50, blank=True, null=True)  # 用户名
    ip = models.CharField(max_length=100, blank=True, null=True)  # 登录IP
    ua = models.CharField(max_length=200, blank=True, null=True)  # 用户代理（User-Agent）
    log_time = models.DateTimeField(auto_now_add=True, null=True)  # 登录时间

    class Meta:
        db_table = "b_login_log"


class OpLog(models.Model):
    """
    操作日志模型
    用于记录系统操作日志，包括请求IP、URL、方法、耗时等
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    re_ip = models.CharField(max_length=100, blank=True, null=True)  # 请求IP
    re_time = models.DateTimeField(auto_now_add=True, null=True)  # 请求时间
    re_url = models.CharField(max_length=200, blank=True, null=True)  # 请求URL
    re_method = models.CharField(max_length=10, blank=True, null=True)  # 请求方法（GET、POST等）
    re_content = models.CharField(max_length=200, blank=True, null=True)  # 请求内容
    access_time = models.CharField(max_length=10, blank=True, null=True)  # 请求耗时（毫秒）

    class Meta:
        db_table = "b_op_log"


class ErrorLog(models.Model):
    """
    错误日志模型
    用于记录系统错误日志信息
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    ip = models.CharField(max_length=100, blank=True, null=True)  # 错误发生时的IP
    url = models.CharField(max_length=200, blank=True, null=True)  # 错误发生的URL
    method = models.CharField(max_length=10, blank=True, null=True)  # 请求方法
    content = models.CharField(max_length=200, blank=True, null=True)  # 错误内容
    log_time = models.DateTimeField(auto_now_add=True, null=True)  # 错误发生时间

    class Meta:
        db_table = "b_error_log"


class Order(models.Model):
    """
    订单模型
    用于存储订单信息，包括订单状态、支付信息、收货信息等
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    order_number = models.CharField(max_length=13, blank=True, null=True)  # 订单号
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_order')  # 用户外键
    gwc = models.CharField(max_length=512, blank=True, null=True)  # 购物车商品信息（JSON字符串）
    amount = models.CharField(max_length=10, blank=True, null=True)  # 订单金额
    status = models.CharField(max_length=2, blank=True, null=True)  # 订单状态：1-未支付，2-已支付，7-订单取消
    order_time = models.DateTimeField(auto_now_add=True, null=True)  # 订单创建时间
    pay_time = models.DateTimeField(null=True)  # 支付时间
    receiver_name = models.CharField(max_length=20, blank=True, null=True)  # 收货人姓名
    receiver_address = models.CharField(max_length=50, blank=True, null=True)  # 收货地址
    receiver_phone = models.CharField(max_length=20, blank=True, null=True)  # 收货人电话
    remark = models.CharField(max_length=30, blank=True, null=True)  # 订单备注

    class Meta:
        db_table = "b_order"


class OrderLog(models.Model):
    """
    订单日志模型
    用于记录订单操作日志
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_order_log')  # 用户外键
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, null=True, related_name='thing_order_log')  # 商品外键
    action = models.CharField(max_length=2, blank=True, null=True)  # 操作类型
    log_time = models.DateTimeField(auto_now_add=True, null=True)  # 日志时间

    class Meta:
        db_table = "b_order_log"  # 数据库表名


class Banner(models.Model):
    """
    轮播图模型
    用于首页轮播图管理
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    image = models.ImageField(upload_to='banner/', null=True)  # 轮播图片
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, null=True, related_name='thing_banner')  # 关联商品
    create_time = models.DateTimeField(auto_now_add=True, null=True)  # 创建时间

    class Meta:
        db_table = "b_banner"


class Ad(models.Model):
    """
    广告模型
    用于广告管理
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    image = models.ImageField(upload_to='ad/', null=True)  # 广告图片
    link = models.CharField(max_length=500, blank=True, null=True)  # 广告链接
    create_time = models.DateTimeField(auto_now_add=True, null=True)  # 创建时间

    class Meta:
        db_table = "b_ad"


class Notice(models.Model):
    """
    公告模型
    用于系统公告管理
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    title = models.CharField(max_length=100, blank=True, null=True)  # 公告标题
    content = models.CharField(max_length=1000, blank=True, null=True)  # 公告内容
    create_time = models.DateTimeField(auto_now_add=True, null=True)  # 创建时间

    class Meta:
        db_table = "b_notice"


class Address(models.Model):
    """
    地址模型
    用于存储用户的收货地址信息
    """
    id = models.BigAutoField(primary_key=True)  # 主键ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_address')  # 用户外键
    name = models.CharField(max_length=100, blank=True, null=True)  # 收货人姓名
    mobile = models.CharField(max_length=30, blank=True, null=True)  # 收货人电话
    desc = models.CharField(max_length=300, blank=True, null=True)  # 地址详情
    default = models.BooleanField(blank=True, null=True, default=False)  # 是否默认地址
    create_time = models.DateTimeField(auto_now_add=True, null=True)  # 创建时间

    class Meta:
        db_table = "b_address"
