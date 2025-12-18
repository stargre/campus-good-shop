// API基础URL配置
// 根据当前访问域名动态指向后端，保证在局域网/本机访问都可用
const API_HOST = (typeof window !== 'undefined' && window.location && window.location.hostname) ? window.location.hostname : '127.0.0.1'
const BASE_URL = `http://${API_HOST}:8000/myapp`
const SERVER_ORIGIN = `http://${API_HOST}:8000`

const USER_ID = 'user_id'
const USER_NAME = 'user_name'
const USER_TOKEN = 'user_token'

const ADMIN_USER_ID = 'admin_user_id'
const ADMIN_USER_NAME = 'admin_user_name'
const ADMIN_USER_TOKEN = 'admin_user_token'


export {BASE_URL, SERVER_ORIGIN, USER_TOKEN, USER_NAME, USER_ID, ADMIN_USER_ID,ADMIN_USER_NAME,ADMIN_USER_TOKEN }
