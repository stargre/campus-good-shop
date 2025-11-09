"""
API响应处理器
提供统一的API响应格式
"""
from rest_framework.response import Response


class APIResponse(Response):
    """
    统一的API响应类
    所有API接口使用此类返回响应，保证响应格式一致
    """
    def __init__(self, code=0, msg='', data=None, status=200, headers=None, content_type=None, **kwargs):
        """
        初始化API响应
        Args:
            code (int): 响应码，0表示成功，非0表示失败
            msg (str): 响应消息
            data: 响应数据
            status (int): HTTP状态码
            headers: HTTP头
            content_type: 内容类型
            **kwargs: 其他参数
        """
        dic = {'code': code, 'msg': msg}
        if data is not None:
            dic['data'] = data

        dic.update(kwargs)  # 合并额外参数
        super().__init__(data=dic, status=status,
                         template_name=None, headers=headers,
                         exception=False, content_type=content_type)
