import {get, post} from '/@/utils/http/axios';

enum URL {
  list = '/index/address/list',
  create = '/index/address/create',
  update = '/index/address/update',
  delete = '/index/address/delete',
}

const listApi = async (params: any) =>
    get<any>({url: URL.list, params: params, data: {}, headers: {}});
const createApi = async (data: any) =>
    post<any>({
        url: URL.create,
        params: {},
        data: data,
        // 让Axios为FormData自动设置带boundary的Content-Type
    });
const updateApi = async (params:any, data: any) =>
    post<any>({
        url: URL.update,
        params: params,
        data: data,
    });
const deleteApi = async (params: any) =>
    post<any>({url: URL.delete, params: params, headers: {}});

export {listApi, createApi, updateApi, deleteApi};
