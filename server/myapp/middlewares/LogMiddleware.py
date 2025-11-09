# -*- coding:utf-8 -*-
"""
操作日志中间件
记录所有HTTP请求的操作日志，包括IP、URL、方法、耗时等信息
"""
import time
import json

from django.utils.deprecation import MiddlewareMixin

from myapp import utils
from myapp.serializers import OpLogSerializer


class OpLogs(MiddlewareMixin):
    """
    操作日志中间件类
    拦截所有HTTP请求，记录操作日志
    """

    def __init__(self, *args):
        """
        初始化中间件
        """
        super(OpLogs, self).__init__(*args)

        self.start_time = None  # 请求开始时间
        self.end_time = None  # 请求结束时间
        self.data = {}  # 日志数据字典

    def process_request(self, request):
        """
        处理请求前执行
        记录请求开始时间和基本信息
        Args:
            request: Django请求对象
        """
        self.start_time = time.time()  # 记录开始时间

        # 获取请求基本信息
        re_ip = utils.get_ip(request)  # 请求IP
        re_method = request.method  # 请求方法
        re_content = request.GET if re_method == 'GET' else request.POST  # 请求内容
        if re_content:
            re_content = json.dumps(re_content)
        else:
            re_content = None

        # 保存请求信息
        self.data.update(
            {
                're_url': request.path,  # 请求URL
                're_method': re_method,  # 请求方法
                're_ip': re_ip,  # 请求IP
                # 're_content': re_content,  # 请求内容（已注释，避免日志过大）
            }
        )

    def process_response(self, request, response):
        """
        处理响应后执行
        计算请求耗时并记录日志（当前已注释保存到数据库的代码）
        Args:
            request: Django请求对象
            response: Django响应对象
        Returns:
            response: 响应对象
        """
        # 计算请求耗时（毫秒）
        self.end_time = time.time()  # 记录结束时间
        access_time = self.end_time - self.start_time
        self.data['access_time'] = round(access_time * 1000)  # 转换为毫秒

        # 保存操作日志到数据库（当前已注释，可根据需要开启）
        # serializer = OpLogSerializer(data=self.data)
        # if serializer.is_valid():
        #     serializer.save()

        return response
