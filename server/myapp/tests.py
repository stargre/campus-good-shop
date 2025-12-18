from django.test import TestCase
from rest_framework.test import APIClient
from myapp.models import UserInfo, Product, Category, UserOrder


class OrderProcessTests(TestCase):
    def setUp(self):
        # 创建测试用户与商品
        self.buyer = UserInfo.objects.create(user_student_id='s001', user_password='pw', user_name='buyer', user_email='b@example.com', token='token_b')
        self.seller = UserInfo.objects.create(user_student_id='s002', user_password='pw', user_name='seller', user_email='s@example.com', token='token_s')
        self.category = Category.objects.create(category_name='cat')

    def test_pay_fails_if_product_already_sold(self):
        # 商品已售出
        product = Product.objects.create(user_id=self.seller, category=self.category, product_title='p1', product_o_price=100, product_price=50, product_status=3)
        order = UserOrder.objects.create(user_id=self.buyer, seller_id=self.seller, product_id=product, product_title=product.product_title, price=product.product_price, order_status=0)

        client = APIClient()
        res = client.post('/index/order/pay', {'order_id': order.order_id}, format='json', HTTP_TOKEN=self.buyer.token)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('code'), 1)
        self.assertIn('商品已售出', res.data.get('msg', ''))

    def test_seller_can_refund_before_delivery(self):
        product = Product.objects.create(user_id=self.seller, category=self.category, product_title='p2', product_o_price=100, product_price=50, product_status=3)
        order = UserOrder.objects.create(user_id=self.buyer, seller_id=self.seller, product_id=product, product_title=product.product_title, price=product.product_price, order_status=1)

        client = APIClient()
        res = client.post('/index/order/refund', {'order_id': order.order_id}, format='json', HTTP_TOKEN=self.seller.token)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('code'), 0)
        order.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(order.order_status, 5)
        self.assertEqual(product.product_status, 1)


class ReserveTests(TestCase):
    def setUp(self):
        self.buyer = UserInfo.objects.create(user_student_id='s010', user_password='pw', user_name='buyer2', user_email='b2@example.com', token='token_b2')
        self.seller = UserInfo.objects.create(user_student_id='s011', user_password='pw', user_name='seller2', user_email='s2@example.com', token='token_s2')
        self.category = Category.objects.create(category_name='cat2')
        self.product = Product.objects.create(user_id=self.seller, category=self.category, product_title='p3', product_o_price=100, product_price=50, product_status=1)

    def test_reserve_past_date_rejected(self):
        import datetime
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        client = APIClient()
        res = client.post('/index/product/reserve', {'product_id': self.product.product_id, 'reserve_time': yesterday, 'trade_location': '校门'}, format='json', HTTP_TOKEN=self.buyer.token)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('code'), 1)
        self.assertIn('预约时间不能早于当前时间', res.data.get('msg', ''))

    def test_reserve_today_past_time_rejected(self):
        import datetime
        past_dt = datetime.datetime.now() - datetime.timedelta(hours=2)
        reserve_time = past_dt.strftime('%Y-%m-%d %H:%M')
        client = APIClient()
        res = client.post('/index/product/reserve', {'product_id': self.product.product_id, 'reserve_time': reserve_time, 'trade_location': '校门'}, format='json', HTTP_TOKEN=self.buyer.token)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('code'), 1)
        self.assertIn('预约时间不能早于当前时间', res.data.get('msg', ''))
