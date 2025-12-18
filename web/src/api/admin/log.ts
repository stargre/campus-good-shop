import {get, post} from '/@/utils/http/axios';

enum URL {
  opLogList = '/admin/opLog/list',
  errorLogList = '/admin/errorLog/list',
}

const listOpLogListApi = async (params: any) =>
    get<any>({url: URL.opLogList, params: params, data: {}, headers: {}});
const listErrorLogListApi = async (params: any) =>
    get<any>({url: URL.errorLogList, params: params, data: {}, headers: {}});

export { listOpLogListApi, listErrorLogListApi };
