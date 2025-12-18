from rest_framework.decorators import api_view, authentication_classes
from django.conf import settings
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
import os, time

@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def image(request):
    try:
        file = request.FILES.get('file') or request.FILES.get('image') or None
        if not file:
            return APIResponse(code=1, msg='未找到上传文件')

        subdir = 'cover'
        upload_dir = os.path.join(settings.MEDIA_ROOT, subdir)
        os.makedirs(upload_dir, exist_ok=True)

        ext = os.path.splitext(file.name)[1] or '.jpg'
        filename = f"{int(time.time()*1000)}{ext}"
        save_path = os.path.join(upload_dir, filename)

        with open(save_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        url_path = f"{settings.MEDIA_URL}{subdir}/{filename}"
        return APIResponse(code=0, msg='上传成功', data={'url': url_path})
    except Exception as e:
        return APIResponse(code=1, msg=f'上传失败: {str(e)}')
