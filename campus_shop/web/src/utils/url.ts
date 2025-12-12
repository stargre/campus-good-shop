/**
 * URL处理工具函数
 */

import { SERVER_ORIGIN } from '/@/store/constants'

/**
 * 获取完整的图片URL
 * 数据库存储的路径格式: /upload/avatar/xxx.png 或 /upload/cover/xxx.jpg
 * 前端接收后直接处理，确保是可访问的完整URL
 * @param imageUrl 图片路径（通常已包含/upload/前缀）
 * @returns 完整的图片URL，可直接在<img>标签中使用
 */
export function getImageUrl(imageUrl: string): string {
  if (!imageUrl) {
    return '';
  }

  // 处理空值和非字符串
  const url = String(imageUrl).trim();
  if (!url) {
    return '';
  }

  // 情况1: 如果已经是完整的HTTP(S)URL，直接返回
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url;
  }

  // 情况2: 如果已经以/upload/开头，拼接后端域名，避免前端开发端口请求404
  if (url.startsWith('/upload/')) {
    return `${SERVER_ORIGIN}${url}`;
  }

  // 情况3: 如果是upload/开头（没有前导斜杠），添加斜杠
  if (url.startsWith('upload/')) {
    return `${SERVER_ORIGIN}/` + url;
  }

  // 情况4: 其他情况，补充/upload/前缀并拼后端域名
  return `${SERVER_ORIGIN}/upload/` + url.replace(/^\/+/, '');
}

/**
 * 获取API基础URL
 * @returns API基础URL
 */
export function getApiBaseUrl(): string {
  const protocol = window.location.protocol;
  const host = window.location.host;
  return `${protocol}//${host}`;
}

/**
 * 拼接完整的API URL
 * @param path API路径
 * @returns 完整的API URL
 */
export function getFullApiUrl(path: string): string {
  const baseUrl = getApiBaseUrl();
  // 移除开头的斜杠，避免重复
  const cleanPath = path.startsWith('/') ? path : '/' + path;
  return baseUrl + cleanPath;
}
