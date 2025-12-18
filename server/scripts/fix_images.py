import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from myapp.models import ProductImage

UPLOAD_PREFIX = '/upload/'
COVER_DIR = os.path.join(BASE_DIR, 'upload', 'cover')

def fix():
    rows = ProductImage.objects.all()
    changed = 0
    for r in rows:
        url = r.image_url or ''
        new_url = None
        if url.startswith('/media/products/'):
            basename = os.path.basename(url)
            candidate = os.path.join(COVER_DIR, basename)
            if os.path.exists(candidate):
                new_url = f"{UPLOAD_PREFIX}cover/{basename}"
            else:
                new_url = f"{UPLOAD_PREFIX}cover/1.jpg"
        elif url.startswith('blob:'):
            new_url = f"{UPLOAD_PREFIX}cover/1.jpg"
        if new_url and new_url != url:
            r.image_url = new_url
            r.save(update_fields=['image_url'])
            changed += 1
    print(f"Updated {changed} rows")

if __name__ == '__main__':
    fix()

