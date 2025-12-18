import request from '../../utils/http/axios/index'
import { AxiosResponse } from 'axios'
import { get, post } from '/@/utils/http/axios';

/**
 * 商品相关API
 * 校园闲置物品交易平台
 */

// 商品列表查询参数
interface ProductListParams {
  page?: number
  size?: number
  categoryId?: number
  keyword?: string
  status?: number
  sortBy?: string
  order?: 'asc' | 'desc'
  minPrice?: number
  maxPrice?: number
}

// 商品详情
interface ProductDetail {
  id: number
  name: string
  description: string
  price: number
  images: string[]
  categoryId: number
  categoryName: string
  sellerId: number
  sellerName: string
  sellerAvatar: string
  condition: number
  conditionText: string
  viewCount: number
  createTime: string
  status: number
  statusText: string
}

// 商品创建/更新参数
interface ProductFormData {
  name: string
  description: string
  price: number
  images: string[]
  categoryId: number
  condition: number
  status: number
}

/**
 * 获取商品列表
 */
export const getProductList = (params: ProductListParams): Promise<AxiosResponse> => {
  return request({
    url: '/index/product/list',
    method: 'get',
    params
  })
}

/**
 * 获取商品详情
 */
export const getProductDetail = (id: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/product/detail',
    method: 'get',
    params: { id }
  })
}

/**
 * 创建商品
 */
export const createProduct = (data: ProductFormData): Promise<AxiosResponse> => {
  return request({
    url: '/index/product/create',
    method: 'post',
    data
  })
}

/**
 * 更新商品
 */
export const updateProduct = (id: number, data: ProductFormData): Promise<AxiosResponse> => {
  return request({
    url: '/index/product/update',
    method: 'post',
    data: {
      id,
      ...data
    }
  })
}

/**
 * 删除商品
 */
export const deleteProduct = (id: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/product/delete',
    method: 'post',
    data: { id }
  })
}

/**
 * 获取我的商品列表
 */
export const getMyProductList = (params: any): Promise<AxiosResponse> => {
  return request({
    url: '/index/product/myList',
    method: 'get',
    params
  })
}

/**
 * 预约商品
 */
export const reserveProductApi = async (data: any): Promise<AxiosResponse> => post<any>({ url: '/index/product/reserve', data })

// 收藏相关API
enum COLLECT_URL {
    addCollectUser = '/index/favorite/add',
    getCollectProductList = '/index/favorite/list',
    removeCollectUser = '/index/favorite/remove'
}

/**
 * 添加商品到收藏
 */
export const addProductCollectUserApi = async (params: any) => post<any>({ url: COLLECT_URL.addCollectUser, params: params, headers: {} });

/**
 * 获取收藏商品列表
 */
export const getProductCollectListApi = async (params: any) => get<any>({ url: COLLECT_URL.getCollectProductList, params: params, headers: {} });

/**
 * 移除收藏
 */
export const removeProductCollectUserApi = async (params: any) => post<any>({ url: COLLECT_URL.removeCollectUser, params: params, headers: {} });

// 保留原有API名称作为别名以兼容现有代码
export const listApi = getProductList;
export const detailApi = (params: any) => getProductDetail(params.id);
export const addCollectUserApi = addProductCollectUserApi;
export const removeCollectUserApi = removeProductCollectUserApi;
