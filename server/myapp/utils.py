"""
工具函数模块
提供系统中常用的工具函数，如时间戳、MD5加密、IP获取、错误日志等
"""
import datetime
import hashlib
import time

from rest_framework.views import exception_handler


def get_timestamp():
    """
    获取当前时间戳（毫秒）
    Returns:
        int: 时间戳（毫秒）
    """
    return int(round(time.time() * 1000))


def md5value(key):
    """
    MD5加密函数
    Args:
        key (str): 需要加密的字符串
    Returns:
        str: MD5加密后的字符串（小写）
    """
    input_name = hashlib.md5()
    input_name.update(key.encode("utf-8"))
    md5str = (input_name.hexdigest()).lower()
    print('计算md5:', md5str)
    return md5str


def dict_fetchall(cursor):
    """
    将数据库游标结果转换为字典列表
    Args:
        cursor: 数据库游标对象
    Returns:
        list: 字典列表
    """
    columns = [col[0] for col in cursor.description]  # 获取字段名列表
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def get_ip(request):
    """
    获取请求者的IP地址
    Args:
        request: Django请求对象
    Returns:
        str: IP地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 取第一个IP（如果有代理）
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_ua(request):
    """
    获取请求者的User-Agent信息
    Args:
        request: Django请求对象
    Returns:
        str: User-Agent字符串（最多200字符）
    """
    ua = request.META.get('HTTP_USER_AGENT')
    return ua[0:200] if ua else ''


def getWeekDays():
    """
    获取近一周的日期列表
    Returns:
        list: 日期字符串列表，格式为 'YYYY-MM-DD'
    """
    week_days = []
    now = datetime.datetime.now()
    for i in range(7):
        day = now - datetime.timedelta(days=i)
        week_days.append(day.strftime('%Y-%m-%d %H:%M:%S.%f')[:10])
    week_days.reverse()  # 逆序，从早到晚
    return week_days


def get_monday():
    """
    获取本周周一的日期
    Returns:
        str: 周一日期字符串，格式为 'YYYY-MM-DD'
    """
    now = datetime.datetime.now()
    monday = now - datetime.timedelta(now.weekday())  # 计算本周周一
    return monday.strftime('%Y-%m-%d %H:%M:%S.%f')[:10]


def log_error(request, content):
    """
    记录错误日志到数据库
    Args:
        request: Django请求对象
        content (str): 错误内容
    """
    # 注意：BError 表已被删除，该函数仅保留空实现
    pass
