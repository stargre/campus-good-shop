// 权限问题后期增加
import { get, post } from '/@/utils/http/axios';
import { UserState } from '/@/store/modules/user/types';
// import axios from 'axios';
enum URL {
    userWishList = '/api/productWish/getUserWishList',
    wish = '/api/productWish/wish',
    unWish = '/api/productWish/unWish',
}

const addProductWishUserApi = async (data: any) => post<any>({ url: URL.wish, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const removeProductWishUserApi = async (params: any) => post<any>({ url: URL.unWish, params: params, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const getUserWishListApi = async (params: any) => get<any>({ url: URL.userWishList, params: params });

export { addProductWishUserApi, removeProductWishUserApi, getUserWishListApi };
