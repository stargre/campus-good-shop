import {get, post} from '/@/utils/http/axios';

enum URL {
  list = '/admin/notice/list',
  create = '/admin/notice/create',
  update = '/admin/notice/update',
  delete = '/admin/notice/delete',
}

const listApi = async (params: any) =>
    get<any>({url: URL.list, params: params, data: {}, headers: {}});
const createApi = async (data: any) =>
    post<any>({
        url: URL.create,
        params: {},
        data: data,
    });
const updateApi = async (params: any, data: any) =>
    post<any>({
        url: URL.update,
        data: { ...params, ...data },
    });
const deleteApi = async (params: any) =>
    post<any>({url: URL.delete, params: params, headers: {}});

export {listApi, createApi, updateApi, deleteApi};
