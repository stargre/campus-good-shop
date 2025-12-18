import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from myapp.models import ProductImage, UserInfo

def inspect():
    rows = ProductImage.objects.all().order_by('product_id')
    print(f"Total ProductImage rows: {rows.count()}")
    for r in rows[:200]:
        print({
            'product_id': getattr(r.product_id, 'product_id', None),
            'image_url': r.image_url,
        })
    users = UserInfo.objects.all()[:50]
    print(f"Total UserInfo sample: {users.count()}")
    for u in users:
        print({'user_id': u.user_id, 'user_avart': u.user_avart})

if __name__ == '__main__':
    inspect()
