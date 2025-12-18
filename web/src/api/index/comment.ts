import {get, post} from '/@/utils/http/axios';

enum URL {
  create = '/index/comment/create',
  listProductComments = '/index/comment/list',
  listUserComments = '/index/comment/myList',
  like = '/index/comment/like',
  delete = '/index/comment/delete'
}

const createApi = async (data: any) => post<any>({
    url: URL.create,
    params: {},
    data: data,
});
const listProductCommentsApi = async (params: any) => get<any>({url: URL.listProductComments, params: params, data: {}, headers: {}});
const listUserCommentsApi = async (params: any) => get<any>({url: URL.listUserComments, params: params, data: {}, headers: {}});
const likeApi = async (params: any) => post<any>({url: URL.like, params: params, headers: {}});
const deleteApi = async (params: any) => post<any>({url: URL.delete, params: params, headers: {}});

export {createApi, listProductCommentsApi,listUserCommentsApi, likeApi, deleteApi};
