
import { get, post } from '/@/utils/http/axios';
import { UserState } from '/@/store/modules/user/types';

enum URL {
    userCollectList = '/api/productCollect/getUserCollectList',
    collect = '/api/productCollect/collect',
    unCollect = '/api/productCollect/unCollect',
}

const addProductCollectUserApi = async (data: any) => post<any>({ url: URL.collect, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const removeProductCollectUserApi = async (params: any) => post<any>({ url: URL.unCollect, params: params, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const getUserCollectListApi = async (params: any) => get<any>({ url: URL.userCollectList, params: params });

export { addProductCollectUserApi, removeProductCollectUserApi, getUserCollectListApi };
