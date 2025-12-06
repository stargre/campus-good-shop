import {get, post} from '/@/utils/http/axios';

enum URL {
    create = '/myapp/index/comment/create',
    listProductComments = '/myapp/index/comment/list',
    listUserComments = '/myapp/index/comment/listMyComments',
    like = '/myapp/index/comment/like'
}

const createApi = async (data: any) => post<any>({
    url: URL.create,
    params: {},
    data: data,
    headers: {'Content-Type': 'multipart/form-data;charset=utf-8'}
});
const listProductCommentsApi = async (params: any) => get<any>({url: URL.listProductComments, params: params, data: {}, headers: {}});
const listUserCommentsApi = async (params: any) => get<any>({url: URL.listUserComments, params: params, data: {}, headers: {}});
const likeApi = async (params: any) => post<any>({url: URL.like, params: params, headers: {}});

export {createApi, listProductCommentsApi,listUserCommentsApi, likeApi};
