// 权限问题后期增加
import { get, post } from '/@/utils/http/axios';
import { UserState } from '/@/store/modules/user/types';
// import axios from 'axios';
enum URL {
  userLogin = '/index/user/login',
  userRegister = '/index/user/register',
  detail = '/index/user/info',
  updateUserPwd = '/index/user/updatePwd',
  passwordResetRequest = '/index/user/passwordResetRequest',
  passwordResetVerify = '/index/user/passwordResetVerify',
  passwordResetConfirm = '/index/user/passwordResetConfirm',
  updateUserInfo = '/index/user/update'
}
interface LoginRes {
    token: string;
}

export interface LoginData {
    username: string;
    password: string;
}

const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, data: {}, headers: {} });
const userLoginApi = async (data: LoginData) => post<any>({ url: URL.userLogin, data });
const userRegisterApi = async (data: any) => post<any>({ url: URL.userRegister, params: {}, data: data });
const updateUserPwdApi = async (params: any, data:any) => post<any>({ url: URL.updateUserPwd, params: params, data:data });
const passwordResetRequestApi = async (data: any) => post<any>({ url: URL.passwordResetRequest, data });
const passwordResetVerifyApi = async (data: any) => post<any>({ url: URL.passwordResetVerify, data });
const passwordResetConfirmApi = async (data: any) => post<any>({ url: URL.passwordResetConfirm, data });
const updateUserInfoApi = async (params?: any, data?: any) => {
  // 兼容两种调用方式：updateUserInfoApi(formData) 或 updateUserInfoApi(params, formData)
  const isFormData = (val: any) => typeof FormData !== 'undefined' && val instanceof FormData
  if (data === undefined) {
    const payload = params
    if (isFormData(payload)) {
      return post<any>({ url: URL.updateUserInfo, data: payload, headers: { 'Content-Type': 'multipart/form-data' } });
    }
    return post<any>({ url: URL.updateUserInfo, data: payload });
  }
  if (isFormData(data)) {
    return post<any>({ url: URL.updateUserInfo, params, data, headers: { 'Content-Type': 'multipart/form-data' } });
  }
  return post<any>({ url: URL.updateUserInfo, params, data });
};

export { detailApi, userLoginApi, userRegisterApi, updateUserPwdApi, updateUserInfoApi, passwordResetRequestApi, passwordResetVerifyApi, passwordResetConfirmApi };
