import {get, post} from '/@/utils/http/axios';

const listApi = async (params: any) => {
  // 尝试优先使用 list_api；失败则回退到 list
  try {
    return await get<any>({ url: '/index/notice/list_api', params, data: {}, headers: {} })
  } catch (e) {
    return await get<any>({ url: '/index/notice/list', params, data: {}, headers: {} })
  }
}

export {listApi};
