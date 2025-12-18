// 权限问题后期增加
import { get, post } from '/@/utils/http/axios';
import { UserState } from '/@/store/modules/user/types';
// import axios from 'axios';
enum URL {
    login = '/admin/adminLogin',
    userList = '/admin/user/list',
    detail = '/admin/user/info',
    create = '/admin/user/create',
    update = '/admin/user/update',
    delete = '/admin/user/delete',
    userLogin = '/index/user/login',
    userRegister = '/index/user/register',
    updateUserPwd = '/admin/user/updatePwd',
    updateUserInfo = '/admin/user/update'
}
interface LoginRes {
    token: string;
}

export interface LoginData {
    username: string;
    password: string;
}

const loginApi = async (data: LoginData) => post<any>({ url: URL.login, data });
const listApi = async (params: any) => get<any>({ url: URL.userList, params: params, data: {}, headers: {} });
const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, data: {}, headers: {} });
const createApi = async (data: any) => post<any>({ url: URL.create, data });
const updateApi = async (params: any, data: any) => post<any>({ url: URL.update, params, data });
const deleteApi = async (params: any) => post<any>({ url: URL.delete, params: params, headers: {} });
const userLoginApi = async (data: LoginData) => post<any>({ url: URL.userLogin, data });
const userRegisterApi = async (data: any) => post<any>({ url: URL.userRegister, data });
const updateUserPwdApi = async (params: any) => post<any>({ url: URL.updateUserPwd, params: params });
const updateUserInfoApi = async (params: any, data: any) => post<any>({ url: URL.updateUserInfo, params, data });

export { loginApi, listApi, detailApi, createApi, updateApi, deleteApi, userLoginApi, userRegisterApi, updateUserPwdApi, updateUserInfoApi};
