import request from '/@/utils/http/axios/index'
import { AxiosResponse } from 'axios'

/**
 * 订单相关API
 * 校园二手交易平台
 */

// 订单状态枚举
export enum OrderStatus {
  PENDING_PAYMENT = 1,  // 待支付
  PAID = 2,             // 已支付
  COMPLETED = 3,        // 已完成
  EVALUATED = 4,        // 已评价
  CANCELLED = 5         // 已取消
}

// 订单信息
interface Order {
  id: number
  orderNumber: string
  productId: number
  productName: string
  productImage: string
  price: number
  buyerId: number
  buyerName: string
  sellerId: number
  sellerName: string
  status: number
  statusText: string
  createTime: string
  payTime?: string
  confirmTime?: string
  evaluationContent?: string
  evaluationRating?: number
  evaluationTime?: string
}

// 创建订单参数
interface CreateOrderParams {
  productId: number
  buyerId: number
  sellerId: number
  price: number
}

// 评价订单参数
interface EvaluateOrderParams {
  id: number
  content: string
  rating: number
}

/**
 * 获取订单列表
 */
export const getOrderList = (params: { userId: number; orderStatus?: string }): Promise<AxiosResponse> => {
  return request({
    url: '/index/order/list',
    method: 'get',
    params
  })
}

/**
 * 获取订单详情
 */
export const getOrderDetail = (id: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/order/detail',
    method: 'get',
    params: { id }
  })
}

/**
 * 创建订单
 */
export const createOrder = (data: CreateOrderParams): Promise<AxiosResponse> => {
  return request({
    url: '/index/order/create',
    method: 'post',
    data
  })
}

/**
 * 取消订单
 */
export const cancelOrder = (id: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/order/cancel',
    method: 'post',
    params: { id }
  })
}

/**
 * 支付订单
 */
export const payOrder = (id: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/order/pay',
    method: 'post',
    data: { id }
  })
}

/**
 * 确认收货
 */
export const confirmReceipt = (id: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/order/confirm',
    method: 'post',
    data: { id }
  })
}

/**
 * 评价订单
 */
export const evaluateOrder = (data: EvaluateOrderParams): Promise<AxiosResponse> => {
  return request({
    url: '/index/order/evaluate',
    method: 'post',
    data
  })
}

/**
 * 预约管理相关API
 */

// 预约信息
interface Reserve {
  id: number
  productId: number
  productName: string
  productImage: string
  userId: number
  userName: string
  status: number
  statusText: string
  createTime: string
}

/**
 * 创建预约
 */
export const createReserve = (productId: number, userId: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/reserve/create',
    method: 'post',
    data: { productId, userId }
  })
}

/**
 * 获取预约列表
 */
export const getReserveList = (userId: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/reserve/list',
    method: 'get',
    params: { userId }
  })
}

/**
 * 取消预约
 */
export const cancelReserve = (id: number): Promise<AxiosResponse> => {
  return request({
    url: '/index/reserve/cancel',
    method: 'post',
    data: { id }
  })
}
