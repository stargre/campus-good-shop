"""
API限流模块
限制API请求频率，防止恶意请求
"""
from rest_framework.throttling import AnonRateThrottle


class MyRateThrottle(AnonRateThrottle):
    """
    API限流类
    限制匿名用户请求频率为5次/分钟
    """
    THROTTLE_RATES = {"anon": "5/min"}  # 匿名用户限流：5次/分钟
