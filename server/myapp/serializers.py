"""
序列化器定义模块
定义了校园闲置物品交易平台的所有数据序列化器
"""
from rest_framework import serializers
from .models import (
    UserInfo, Category, Product, ProductImage, Address, 
    UserOrder, Comment, Record, BNotice, 
    Favorite
)


class UserInfoSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    处理前端与后端字段映射问题
    """
    # 前端字段到后端字段的映射
    id = serializers.IntegerField(source='user_id', read_only=True)
    username = serializers.CharField(source='user_student_id', required=True, max_length=50)
    password = serializers.CharField(write_only=True, required=False, max_length=255)
    nickname = serializers.CharField(source='user_name', required=True, max_length=50)
    status = serializers.CharField(source='user_status', required=True)
    email = serializers.CharField(source='user_email', required=True, max_length=50)
    mobile = serializers.CharField(source='user_mobile', required=False, allow_blank=True, allow_null=True, max_length=20)
    # 头像字段兼容：输出为 avatar，内部存储 user_avart
    avatar = serializers.CharField(source='user_avart', read_only=True)

    class Meta:
        model = UserInfo
        fields = ['id', 'user_id', 'user_student_id', 'username', 'user_name', 'nickname', 'user_collage', 
                 'user_email', 'email', 'user_mobile', 'mobile', 'user_create_time', 'user_status', 'status', 'user_avart', 'avatar', 'token', 'password', 'role']
    
    def create(self, validated_data):
        # 处理密码字段映射
        if 'password' in validated_data:
            validated_data['user_password'] = validated_data.pop('password')
        # 处理email字段映射
        if 'email' in validated_data:
            validated_data['user_email'] = validated_data.pop('email')
        # 处理mobile字段映射
        if 'mobile' in validated_data:
            validated_data['user_mobile'] = validated_data.pop('mobile')
        # 统一前端状态语义（前端：0=正常,1=封号；后端：1=正常,0=禁用）
        if 'user_status' in validated_data:
            s = validated_data['user_status']
            validated_data['user_status'] = 1 if str(s) == '0' else 0 if str(s) == '1' else s
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # 处理密码字段映射
        if 'password' in validated_data:
            validated_data['user_password'] = validated_data.pop('password')
        # 处理email字段映射
        if 'email' in validated_data:
            validated_data['user_email'] = validated_data.pop('email')
        # 处理mobile字段映射
        if 'mobile' in validated_data:
            validated_data['user_mobile'] = validated_data.pop('mobile')
        # 统一前端状态语义（前端：0=正常,1=封号；后端：1=正常,0=禁用）
        if 'user_status' in validated_data:
            s = validated_data['user_status']
            validated_data['user_status'] = 1 if str(s) == '0' else 0 if str(s) == '1' else s
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 输出时保持前端语义一致：0=正常,1=封号
        if 'status' in data:
            data['status'] = '0' if str(data['status']) == '1' else '1'
        # 确保mobile字段存在
        if 'mobile' not in data:
            data['mobile'] = instance.user_mobile if hasattr(instance, 'user_mobile') else None
        # 确保avatar字段存在
        if 'avatar' not in data:
            data['avatar'] = instance.user_avart if hasattr(instance, 'user_avart') else ''
        return data
        
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
    # 添加前端需要的字段映射
    id = serializers.IntegerField(source='category_id', read_only=True)
    title = serializers.CharField(source='category_name', required=False)
    
    class Meta:
        model = Category
        fields = ['category_id', 'id', 'category_name', 'title', 'category_sort_order', 'category_create_time']


class ProductImageSerializer(serializers.ModelSerializer):
    """
    商品图片序列化器
    """
    class Meta:
        model = ProductImage
        fields = ['image_id', 'product_id', 'image_url', 'sort_order']


class ProductSerializer(serializers.ModelSerializer):
    """
    商品序列化器（基础信息）
    """
    # 添加用户信息字段
    user_name = serializers.CharField(source='user_id.user_name', read_only=True)
    user_collage = serializers.CharField(source='user_id.user_collage', read_only=True)
    user_student_id = serializers.CharField(source='user_id.user_student_id', read_only=True)
    # 添加分类名称字段
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    # 添加第一张图片作为封面
    cover_image = serializers.SerializerMethodField(read_only=True)
    cover = serializers.SerializerMethodField(read_only=True)  # 兼容前端字段名，必须是SerializerMethodField
    
    def get_cover_image(self, obj):
        # 优先使用 cover_image_id 指向的主图（如果存在），否则回退到按顺序的第一张图片
        if getattr(obj, 'cover_image_id', None):
            try:
                pi = ProductImage.objects.get(pk=obj.cover_image_id)
                return pi.image_url
            except ProductImage.DoesNotExist:
                pass
        images = ProductImage.objects.filter(product_id=obj.product_id).order_by('sort_order')
        if images.exists():
            return images.first().image_url
        return ''
    
    def get_cover(self, obj):
        # 与 get_cover_image 逻辑相同，优先使用 cover_image_id
        if getattr(obj, 'cover_image_id', None):
            try:
                pi = ProductImage.objects.get(pk=obj.cover_image_id)
                return pi.image_url
            except ProductImage.DoesNotExist:
                pass
        images = ProductImage.objects.filter(product_id=obj.product_id).order_by('sort_order')
        if images.exists():
            return images.first().image_url
        return ''
    
    # 将价格从分转换为元
    product_price_yuan = serializers.SerializerMethodField(read_only=True)
    product_o_price_yuan = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)  # 兼容前端字段名
    
    def get_product_price_yuan(self, obj):
        return obj.product_price
    
    def get_product_o_price_yuan(self, obj):
        return obj.product_o_price
    
    def get_price(self, obj):
        return obj.product_price
    
    # 获取商品成色描述
    quality_text = serializers.SerializerMethodField(read_only=True)
    
    def get_quality_text(self, obj):
        quality_map = {1: '全新', 2: '几乎全新', 3: '轻微使用痕迹', 4: '明显使用痕迹'}
        return quality_map.get(obj.quality, '未知')
    
    # 添加前端期望的字段映射
    id = serializers.IntegerField(source='product_id', read_only=True)
    title = serializers.CharField(source='product_title', required=False)
    location = serializers.SerializerMethodField(read_only=True)  # 添加location字段，使用模拟数据
    
    def get_location(self, obj):
        # 优先返回商品的交易地点（如果存在），其次回退到发布者的学院信息
        if hasattr(obj, 'location') and obj.location:
            return obj.location
        try:
            return obj.user_id.user_collage or '未知地点'
        except Exception:
            return '未知地点'
    
    is_reserved = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'id', 'user_id', 'user_name', 'user_collage', 'user_student_id', 'category', 'category_name',
            'product_title', 'title', 'product_o_price', 'product_o_price_yuan', 'product_price', 
            'product_price_yuan', 'price', 'product_status', 'quality', 'quality_text', 'create_time',
            'update_time', 'view_count', 'collect_count', 'cover_image', 'cover', 'is_reserved',
            'location', 'content'
        ]
    
    def update(self, instance, validated_data):
        # 确保产品标题可以通过title或product_title字段更新
        if 'product_title' not in validated_data and 'title' in validated_data:
            validated_data['product_title'] = validated_data.pop('title')
        return super().update(instance, validated_data)


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
        return obj.product_price
    
    def get_product_o_price_yuan(self, obj):
        return obj.product_o_price
    
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
    
    is_reserved = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'user_id', 'user_name', 'user_student_id', 'user_email',
                'category', 'category_name', 'product_title', 'product_o_price', 
                'product_o_price_yuan', 'product_price', 'product_price_yuan', 
            'product_status', 'product_status_text', 'quality', 'quality_text',
            'reject_reason', 'create_time', 'update_time', 'content', 'view_count',
                'collect_count', 'images', 'is_reserved', 'location'
        ]


class AddressSerializer(serializers.ModelSerializer):
    """
    地址序列化器
    """
    class Meta:
        model = Address
        fields = ['address_id', 'user_id', 'receiver_name', 'receiver_phone', 'receiver_address', 'is_default']




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
        status_map = {0: '待支付', 1: '已支付', 2: '已发货', 3: '已完成', 4: '已取消', 5: '已退款'}
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
    buyer_avatar = serializers.CharField(source='user_id.user_avart', read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)  # 兼容前端字段名
    user_avatar = serializers.SerializerMethodField(read_only=True)  # 备选字段名
    # 添加卖家信息
    seller_name = serializers.CharField(source='seller_id.user_name', read_only=True)
    seller_avatar = serializers.CharField(source='seller_id.user_avart', read_only=True)
    # 添加商品标题
    product_title = serializers.CharField(source='product_id.product_title', read_only=True)
    # 获取评论状态描述
    comment_status_text = serializers.SerializerMethodField(read_only=True)
    
    def get_comment_status_text(self, obj):
        status_map = {0: '正常', 1: '隐藏'}
        return status_map.get(obj.comment_status, '未知')
    
    def get_avatar(self, obj):
        # 返回买家头像
        return obj.user_id.user_avart if obj.user_id else ''
    
    def get_user_avatar(self, obj):
        # 返回买家头像（备选字段名）
        return obj.user_id.user_avart if obj.user_id else ''
    
    class Meta:
        model = Comment
        fields = [
            'comment_id', 'order_id', 'product_id', 'product_title', 'user_id', 'buyer_name', 'buyer_avatar',
            'avatar', 'user_avatar', 'seller_id', 'seller_name', 'seller_avatar', 'comment_content', 'rating', 
            'comment_status', 'comment_status_text', 'create_time', 'comment_time', 'like_count'
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
        return obj.product_id.product_price
    
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




class ListProductSerializer(serializers.ModelSerializer):
    """
    商品列表序列化器（用于列表展示，信息更简洁）
    """
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    cover_image = serializers.SerializerMethodField(read_only=True)
    cover = serializers.SerializerMethodField(read_only=True)  # 兼容前端字段名，必须是SerializerMethodField
    product_price_yuan = serializers.SerializerMethodField(read_only=True)
    
    # 添加前端期望的字段映射
    id = serializers.IntegerField(source='product_id', read_only=True)
    title = serializers.CharField(source='product_title', read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    location = serializers.SerializerMethodField(read_only=True)  # 添加location字段，使用模拟数据
    
    def get_cover_image(self, obj):
        # 优先使用 cover_image_id 指向的主图（如果存在），否则回退到按顺序的第一张图片
        if getattr(obj, 'cover_image_id', None):
            try:
                pi = ProductImage.objects.get(pk=obj.cover_image_id)
                return pi.image_url
            except ProductImage.DoesNotExist:
                pass
        images = ProductImage.objects.filter(product_id=obj.product_id).order_by('sort_order')
        if images.exists():
            return images.first().image_url
        return ''
    
    def get_cover(self, obj):
        # 与 get_cover_image 逻辑相同，优先使用 cover_image_id
        if getattr(obj, 'cover_image_id', None):
            try:
                pi = ProductImage.objects.get(pk=obj.cover_image_id)
                return pi.image_url
            except ProductImage.DoesNotExist:
                pass
        images = ProductImage.objects.filter(product_id=obj.product_id).order_by('sort_order')
        if images.exists():
            return images.first().image_url
        return ''
    
    def get_product_price_yuan(self, obj):
        return obj.product_price
    
    def get_price(self, obj):
        return obj.product_price
    
    def get_location(self, obj):
        # 这里可以根据实际情况从数据库获取位置信息
        # 如果数据库中没有location字段，可以返回一个默认值
        return "默认位置"  # 临时默认值
    
    is_reserved = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'id', 'product_title', 'title', 'category_name', 'product_price', 
            'product_price_yuan', 'price', 'product_status', 'cover_image', 'cover', 'create_time', 'view_count', 'is_reserved', 'location'
        ]


class ListUserOrderSerializer(serializers.ModelSerializer):
    """
    订单列表序列化器（用于列表展示，信息更简洁）
    """
    # 添加买家与卖家信息供管理端展示
    buyer_name = serializers.CharField(source='user_id.user_name', read_only=True)
    seller_name = serializers.CharField(source='seller_id.user_name', read_only=True)

    order_status_text = serializers.SerializerMethodField(read_only=True)
    
    def get_order_status_text(self, obj):
        status_map = {0: '待支付', 1: '已支付', 2: '已发货', 3: '已完成', 4: '已取消', 5: '已退款'}
        return status_map.get(obj.order_status, '未知')
    
    class Meta:
        model = UserOrder
        fields = [
            'order_id', 'product_title', 'price', 'order_status', 
            'order_status_text', 'create_time', 'pay_time', 'buyer_name', 'seller_name'
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    """
    收藏序列化器
    """
    # 添加商品信息
    product_title = serializers.CharField(source='product_id.product_title', read_only=True)
    product_price = serializers.IntegerField(source='product_id.product_price', read_only=True)
    product_price_yuan = serializers.SerializerMethodField(read_only=True)
    product_image = serializers.SerializerMethodField(read_only=True)
    product_status = serializers.IntegerField(source='product_id.product_status', read_only=True)
    
    def get_product_price_yuan(self, obj):
        return obj.product_id.product_price
    
    def get_product_image(self, obj):
        """
        获取商品第一张图片
        """
        images = ProductImage.objects.filter(product_id=obj.product_id).order_by('sort_order')
        if images.exists():
            return images.first().image_url
        return ''
    
    class Meta:
        model = Favorite
        fields = [
            'favorite_id', 'user_id', 'product_id', 'product_title', 'product_price', 
            'product_price_yuan', 'product_image', 'product_status', 'create_time'
        ]


