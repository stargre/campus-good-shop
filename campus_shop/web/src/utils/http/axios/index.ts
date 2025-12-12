/**
 * Axios HTTP请求配置
 * 配置请求拦截器、响应拦截器，统一处理Token和错误
 */
import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { showMessage } from './status';
import { IResponse } from './type';
import { getToken } from '/@/utils/auth';
import { TokenPrefix } from '/@/utils/auth';
import {ADMIN_USER_TOKEN, USER_TOKEN, BASE_URL} from '/@/store/constants'

// 创建Axios实例
const service: AxiosInstance = axios.create({
  // baseURL: import.meta.env.BASE_URL + '',
  baseURL: BASE_URL,  // API基础URL（已包含/myapp路径）
  timeout: 15000,  // 请求超时时间（15秒）
  headers: {
    'Content-Type': 'application/json; charset=utf-8'
  }
});

// ==================== 请求拦截器 ====================
// 在发送请求前统一添加Token到请求头
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 添加后台管理Token到请求头
    config.headers.ADMINTOKEN = localStorage.getItem(ADMIN_USER_TOKEN)
    // 添加前台用户Token到请求头
    config.headers.TOKEN = localStorage.getItem(USER_TOKEN)

    return config;
  },
  (error: AxiosError) => {
    // 请求错误处理
    return Promise.reject(error);
  },
);

// ==================== 响应拦截器 ====================
// 统一处理响应数据
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // HTTP状态码200
    if(response.status == 200) {
      // 业务状态码0或200表示成功
      if(response.data.code == 0 || response.data.code == 200) {
        return response
      }else {
        // 业务失败，返回错误
        return Promise.reject(response.data)
      }
    } else {
      return Promise.reject(response.data)
    }
  },
  // 请求失败处理
  (error: any) => {
    const status = error?.response?.status
    const url = error?.config?.url || ''
    console.log(status)
    if(status == 404) {
      // 404错误处理（待实现）
      // todo
    } else if(status == 403) {
      // 403：鉴权失败，针对后台接口提示并引导登录
      if (typeof window !== 'undefined' && url.includes('/admin/')) {
        try { (window as any).message?.warn?.('管理员权限验证失败，请重新登录') } catch (_) {}
        setTimeout(() => { window.location.href = '/admin' }, 50)
      }
    }
    return Promise.reject(error)
  },
);



const request = <T = any>(config: AxiosRequestConfig): Promise<T> => {
  const conf = config;
  return new Promise((resolve, reject) => {
    service.request<any, AxiosResponse<IResponse>>(conf).then((res: AxiosResponse<IResponse>) => {
      const data = res.data
      resolve(data as T);
    }).catch(err => {
      reject(err)
    });
  });
};

export function get<T = any>(config: AxiosRequestConfig): Promise<T> {
  return request({ ...config, method: 'GET' });
}

export function post<T = any>(config: AxiosRequestConfig): Promise<T> {
  return request({ ...config, method: 'POST' });
}

export default request;

export type { AxiosInstance, AxiosResponse };
