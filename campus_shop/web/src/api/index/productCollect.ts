
import { get, post } from '/@/utils/http/axios';
import { UserState } from '/@/store/modules/user/types';

enum URL {
  userCollectList = '/index/favorite/list',
  collect = '/index/favorite/add',
  unCollect = '/index/favorite/remove',
}

const addProductCollectUserApi = async (data: any) => post<any>({ url: URL.collect, data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const removeProductCollectUserApi = async (data: any) => post<any>({ url: URL.unCollect, data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const getUserCollectListApi = async (params: any) => get<any>({ url: URL.userCollectList, params });

export { addProductCollectUserApi, removeProductCollectUserApi, getUserCollectListApi };
