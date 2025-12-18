import { post } from '/@/utils/http/axios'

enum URL {
  uploadImage = '/index/upload/image',
}

// 使用FormData上传图片，显式指定 multipart/form-data 让后端能解析文件
const uploadImageApi = async (data: FormData) => post<any>({ url: URL.uploadImage, data, headers: { 'Content-Type': 'multipart/form-data' } })

export { uploadImageApi }

