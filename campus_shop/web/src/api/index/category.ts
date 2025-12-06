import request from '../../utils/http/axios/index'
import { AxiosResponse } from 'axios'
import {get, post} from '/@/utils/http/axios';

/**
 * 分类相关API
 * 校园二手交易平台
 */

// 分类信息
interface Category {
  id: number
  name: string
  icon: string
  description: string
  createTime: string
  productCount?: number
}

/**
 * 获取分类列表
 */
export const getCategoryList = (): Promise<AxiosResponse> => {
  return request({
    url: '/index/category/list',
    method: 'get'
  })
}

/**
 * 获取分类详情
 */
export const getCategoryDetail = (id: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/category/detail',
    method: 'get',
    params: { id }
  })
}

/**
 * 获取分类及商品数量
 */
export const getCategoryListWithProducts = (): Promise<AxiosResponse> => {
  return request({
    url: '/index/category/listWithProducts',
    method: 'get'
  })
}

// 分类相关API
enum CATEGORY_URL {
    list = '/myapp/index/category/list',
}

/**
 * 获取分类列表
 */
export const getCategoryListApi = (params: any) => get<any>({url: CATEGORY_URL.list, params: params, data: {}, headers: {}});
// 保留原有API名称作为别名以兼容现有代码
export const listApi = getCategoryListApi;