"""
序列化器定义模块
定义了校园二手交易平台的所有数据序列化器
"""
from rest_framework import serializers
from .models import (
    UserInfo, Category, Product, ProductImage, Address, Cart, 
    UserOrder, Comment, Reserve, Record, BNotice, BLogin, 
    BOp, BError, Tag, ProductTag
)


class UserInfoSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    """
    class Meta:
        model = UserInfo
        fields = ['user_id', 'user_student_id', 'user_name', 'user_collage', 
                 'user_email', 'user_create_time', 'user_status', 'user_avart', 'token']
        
class UserInfoDetailSerializer(serializers.ModelSerializer):
    """
    用户信息详情序列化器（包含密码字段，仅限内部使用）
    """
    class Meta:
        model = UserInfo
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    """
    分类序列化器
    """
    class Meta:
        model = Category
        fields = ['category_id', 'category_name', 'category_sort_order', 'category_create_time']


class ProductImageSerializer(serializers.ModelSerializer):
    """
    商品图片序列化器
    """
    class Meta:
        model = ProductImage
        fields = ['image_id', 'product_id', 'image_url', 'sort_order']


class TagSerializer(serializers.ModelSerializer):
    """
    标签序列化器
    """
    class Meta:
        model = Tag
        fields = ['tag_id', 'tag_name', 'create_time']

class ProductSerializer(serializers.ModelSerializer):
    """
    商品序列化器（基础信息）
    """
    # 添加用户信息字段
    user_name = serializers.CharField(source='user_id.user_name', read_only=True)
    user_student_id = serializers.CharField(source='user_id.user_student_id', read_only=True)
    # 添加分类名称字段
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    # 添加第一张图片作为封面
    cover_image = serializers.SerializerMethodField(read_only=True)
    # 添加标签字段
    tags = TagSerializer(many=True, read_only=True)
    
    def get_cover_image(self, obj):
        """
        获取商品第一张图片作为封面
        """
        images = ProductImage.objects.filter(product_id=obj.product_id).order_by('sort_order')
        if images.exists():
            return images.first().image_url
        return ''
    
    # 将价格从分转换为元
    product_price_yuan = serializers.SerializerMethodField(read_only=True)
    product_o_price_yuan = serializers.SerializerMethodField(read_only=True)
    
    def get_product_price_yuan(self, obj):
        return obj.product_price / 100.0
    
    def get_product_o_price_yuan(self, obj):
        return obj.product_o_price / 100.0
    
    # 获取商品成色描述
    quality_text = serializers.SerializerMethodField(read_only=True)
    
    def get_quality_text(self, obj):
        quality_map = {1: '全新', 2: '几乎全新', 3: '轻微使用痕迹', 4: '明显使用痕迹'}
        return quality_map.get(obj.quality, '未知')
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'user_id', 'user_name', 'user_student_id', 'category', 'category_name',
            'product_title', 'product_o_price', 'product_o_price_yuan', 'product_price', 
            'product_price_yuan', 'product_status', 'quality', 'quality_text', 'create_time',
            'update_time', 'view_count', 'wish_count', 'collect_count', 'cover_image', 'tags'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    商品详情序列化器
    """
    # 添加用户信息字段
    user_name = serializers.CharField(source='user_id.user_name', read_only=True)
    user_student_id = serializers.CharField(source='user_id.user_student_id', read_only=True)
    user_email = serializers.CharField(source='user_id.user_email', read_only=True)
    # 添加分类名称字段
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    # 添加图片列表
    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')
    
    # 将价格从分转换为元
    product_price_yuan = serializers.SerializerMethodField(read_only=True)
    product_o_price_yuan = serializers.SerializerMethodField(read_only=True)
    
    def get_product_price_yuan(self, obj):
        return obj.product_price / 100.0
    
    def get_product_o_price_yuan(self, obj):
        return obj.product_o_price / 100.0
    
    # 获取商品成色描述
    quality_text = serializers.SerializerMethodField(read_only=True)
    # 获取商品状态描述
    product_status_text = serializers.SerializerMethodField(read_only=True)
    
    def get_quality_text(self, obj):
        quality_map = {1: '全新', 2: '几乎全新', 3: '轻微使用痕迹', 4: '明显使用痕迹'}
        return quality_map.get(obj.quality, '未知')
    
    def get_product_status_text(self, obj):
        status_map = {0: '待审核', 1: '审核通过', 2: '审核不通过', 3: '已售出'}
        return status_map.get(obj.product_status, '未知')
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'user_id', 'user_name', 'user_student_id', 'user_email',
            'category', 'category_name', 'product_title', 'product_o_price', 
            'product_o_price_yuan', 'product_price', 'product_price_yuan', 
            'product_status', 'product_status_text', 'quality', 'quality_text',
            'reject_reason', 'create_time', 'update_time', 'content', 'view_count',
            'wish_count', 'collect_count', 'images'
        ]


class AddressSerializer(serializers.ModelSerializer):
    """
    地址序列化器
    """
    class Meta:
        model = Address
        fields = ['address_id', 'user_id', 'receiver_name', 'receiver_phone', 'receiver_address', 'is_default']


class CartSerializer(serializers.ModelSerializer):
    """
    购物车序列化器
    """
    # 添加商品信息
    product_title = serializers.CharField(source='product_id.product_title', read_only=True)
    product_price = serializers.IntegerField(source='product_id.product_price', read_only=True)
    product_price_yuan = serializers.SerializerMethodField(read_only=True)
    product_image = serializers.SerializerMethodField(read_only=True)
    
    def get_product_price_yuan(self, obj):
        return obj.product_id.product_price / 100.0
    
    def get_product_image(self, obj):
        """
        获取商品第一张图片
        """
        images = ProductImage.objects.filter(product_id=obj.product_id).order_by('sort_order')
        if images.exists():
            return images.first().image_url
        return ''
    
    class Meta:
        model = Cart
        fields = ['cart_id', 'user_id', 'product_id', 'product_title', 'product_price', 'product_price_yuan', 'product_image', 'add_time']


class UserOrderSerializer(serializers.ModelSerializer):
    """
    订单序列化器
    """
    # 添加买家信息
    buyer_name = serializers.CharField(source='user_id.user_name', read_only=True)
    # 添加卖家信息
    seller_name = serializers.CharField(source='seller_id.user_name', read_only=True)
    # 获取订单状态描述
    order_status_text = serializers.SerializerMethodField(read_only=True)
    
    def get_order_status_text(self, obj):
        status_map = {0: '待支付', 1: '已支付', 2: '已发货', 3: '已完成', 4: '已取消', 5: '退款中'}
        return status_map.get(obj.order_status, '未知')
    
    class Meta:
        model = UserOrder
        fields = [
            'order_id', 'user_id', 'buyer_name', 'seller_id', 'seller_name', 
            'product_id', 'product_title', 'product_image', 'price', 
            'order_status', 'order_status_text', 'create_time', 'pay_time',
            'receive_time', 'cancel_time', 'refund_reason'
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    评论序列化器
    """
    # 添加买家信息
    buyer_name = serializers.CharField(source='user_id.user_name', read_only=True)
    # 添加卖家信息
    seller_name = serializers.CharField(source='seller_id.user_name', read_only=True)
    # 获取评论状态描述
    comment_status_text = serializers.SerializerMethodField(read_only=True)
    
    def get_comment_status_text(self, obj):
        status_map = {0: '正常', 1: '隐藏'}
        return status_map.get(obj.comment_status, '未知')
    
    class Meta:
        model = Comment
        fields = [
            'comment_id', 'order_id', 'user_id', 'buyer_name', 'seller_id', 
            'seller_name', 'comment_content', 'rating', 'comment_status', 
            'comment_status_text', 'create_time'
        ]


class ReserveSerializer(serializers.ModelSerializer):
    """
    预约序列化器
    """
    # 添加买家信息
    buyer_name = serializers.CharField(source='user_id.user_name', read_only=True)
    # 添加卖家信息
    seller_name = serializers.CharField(source='seller_id.user_name', read_only=True)
    # 添加地址信息
    receiver_name = serializers.CharField(source='address_id.receiver_name', read_only=True)
    receiver_phone = serializers.CharField(source='address_id.receiver_phone', read_only=True)
    receiver_address = serializers.CharField(source='address_id.receiver_address', read_only=True)
    # 获取预约状态描述
    reserve_status_text = serializers.SerializerMethodField(read_only=True)
    
    def get_reserve_status_text(self, obj):
        status_map = {0: '待确认', 1: '已确认', 2: '已完成', 3: '已取消'}
        return status_map.get(obj.reserve_status, '未知')
    
    class Meta:
        model = Reserve
        fields = [
            'reserve_id', 'order_id', 'user_id', 'buyer_name', 'seller_id', 'seller_name',
            'address_id', 'receiver_name', 'receiver_phone', 'receiver_address', 
            'reserve_status', 'reserve_status_text', 'create_time', 'finish_time'
        ]


class RecordSerializer(serializers.ModelSerializer):
    """
    浏览记录序列化器
    """
    # 添加商品信息
    product_title = serializers.CharField(source='product_id.product_title', read_only=True)
    product_price = serializers.IntegerField(source='product_id.product_price', read_only=True)
    product_price_yuan = serializers.SerializerMethodField(read_only=True)
    product_image = serializers.SerializerMethodField(read_only=True)
    
    def get_product_price_yuan(self, obj):
        return obj.product_id.product_price / 100.0
    
    def get_product_image(self, obj):
        """
        获取商品第一张图片
        """
        images = ProductImage.objects.filter(product_id=obj.product_id).order_by('sort_order')
        if images.exists():
            return images.first().image_url
        return ''
    
    class Meta:
        model = Record
        fields = [
            'record_id', 'user_id', 'product_id', 'product_title', 'product_price', 
            'product_price_yuan', 'product_image', 'create_time'
        ]


class BNoticeSerializer(serializers.ModelSerializer):
    """
    公告序列化器
    """
    class Meta:
        model = BNotice
        fields = ['b_notice_id', 'notice_content', 'create_time', 'sort_value']


class BLoginSerializer(serializers.ModelSerializer):
    """
    登录日志序列化器
    """
    # 添加用户信息
    user_name = serializers.CharField(source='user_id.user_name', read_only=True)
    user_student_id = serializers.CharField(source='user_id.user_student_id', read_only=True)
    
    class Meta:
        model = BLogin
        fields = [
            'b_login_id', 'user_id', 'user_name', 'user_student_id', 'login_time', 
            'ip_address', 'login_device', 'login_status'
        ]


class BOpSerializer(serializers.ModelSerializer):
    """
    操作日志序列化器
    """
    # 添加用户信息
    user_name = serializers.CharField(source='user_id.user_name', read_only=True)
    user_student_id = serializers.CharField(source='user_id.user_student_id', read_only=True)
    
    class Meta:
        model = BOp
        fields = [
            'b_op_id', 'user_id', 'user_name', 'user_student_id', 'op_time', 
            'op_type', 'op_object', 'op_detail'
        ]


class BErrorSerializer(serializers.ModelSerializer):
    """
    错误日志序列化器
    """
    # 添加用户信息
    user_name = serializers.CharField(source='user_id.user_name', read_only=True)
    user_student_id = serializers.CharField(source='user_id.user_student_id', read_only=True)
    
    class Meta:
        model = BError
        fields = [
            'b_error_id', 'user_id', 'user_name', 'user_student_id', 'error_type', 
            'error_code', 'error_time', 'error_message', 'handle_status', 
            'handle_time', 'handle_detail'
        ]


# 以下是用于列表展示的序列化器，提供更简洁的信息
class ListProductSerializer(serializers.ModelSerializer):
    """
    商品列表序列化器（用于列表展示，信息更简洁）
    """
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    cover_image = serializers.SerializerMethodField(read_only=True)
    product_price_yuan = serializers.SerializerMethodField(read_only=True)
    
    def get_cover_image(self, obj):
        """
        获取商品第一张图片作为封面
        """
        images = ProductImage.objects.filter(product_id=obj.product_id).order_by('sort_order')
        if images.exists():
            return images.first().image_url
        return ''
    
    def get_product_price_yuan(self, obj):
        return obj.product_price / 100.0
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'product_title', 'category_name', 'product_price', 
            'product_price_yuan', 'product_status', 'cover_image', 'create_time', 'view_count'
        ]


class ListUserOrderSerializer(serializers.ModelSerializer):
    """
    订单列表序列化器（用于列表展示，信息更简洁）
    """
    order_status_text = serializers.SerializerMethodField(read_only=True)
    
    def get_order_status_text(self, obj):
        status_map = {0: '待支付', 1: '已支付', 2: '已发货', 3: '已完成', 4: '已取消', 5: '退款中'}
        return status_map.get(obj.order_status, '未知')
    
    class Meta:
        model = UserOrder
        fields = [
            'order_id', 'product_title', 'price', 'order_status', 
            'order_status_text', 'create_time', 'pay_time'
        ]
