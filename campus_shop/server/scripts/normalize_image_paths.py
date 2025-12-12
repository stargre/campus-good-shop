import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from myapp.models import ProductImage, UserInfo

MEDIA_URL = '/upload/'
COVER_DIR = os.path.join(BASE_DIR, 'upload', 'cover')
AVATAR_DIR = os.path.join(BASE_DIR, 'upload', 'avatar')

def basename_from_url(url: str) -> str:
    s = url or ''
    if s.startswith('blob:'):
        return ''
    parts = s.split('?')[0].split('#')[0].split('/')
    return parts[-1] if parts else ''

def normalize_product_images():
    if not os.path.isdir(COVER_DIR):
        print('Cover directory not found:', COVER_DIR)
        return
    cover_files = {f.lower(): f for f in os.listdir(COVER_DIR) if os.path.isfile(os.path.join(COVER_DIR, f))}
    fallback = None
    for name in ['1.jpg', '1.jpeg']:
        if name in cover_files:
            fallback = cover_files[name]
            break
    rows = ProductImage.objects.all()
    changed = 0
    for r in rows:
        bn = basename_from_url(r.image_url)
        target_file = cover_files.get(bn.lower()) if bn else None
        if target_file:
            new_url = f"{MEDIA_URL}cover/{target_file}"
        elif fallback:
            new_url = f"{MEDIA_URL}cover/{fallback}"
        else:
            continue
        if new_url != r.image_url:
            r.image_url = new_url
            r.save(update_fields=['image_url'])
            changed += 1
    print(f'ProductImage updated: {changed}')

def normalize_user_avatars():
    if not os.path.isdir(AVATAR_DIR):
        print('Avatar directory not found:', AVATAR_DIR)
        return
    avatar_files = {f.lower(): f for f in os.listdir(AVATAR_DIR) if os.path.isfile(os.path.join(AVATAR_DIR, f))}
    fallback = None
    for name in ['default.jpg', 'default.jpeg', '1676553050529.png']:
        if name in avatar_files:
            fallback = avatar_files[name]
            break
    rows = UserInfo.objects.all()
    changed = 0
    for u in rows:
        bn = basename_from_url(u.user_avart)
        target_file = avatar_files.get(bn.lower()) if bn else None
        if target_file:
            new_url = f"{MEDIA_URL}avatar/{target_file}"
        elif fallback:
            new_url = f"{MEDIA_URL}avatar/{fallback}"
        else:
            continue
        if new_url != u.user_avart:
            u.user_avart = new_url
            u.save(update_fields=['user_avart'])
            changed += 1
    print(f'UserInfo avatars updated: {changed}')

if __name__ == '__main__':
    normalize_product_images()
    normalize_user_avatars()

