/**
 * 路由配置
 * 配置路由守卫，实现权限控制和路由拦截
 */
import {createRouter, createWebHistory} from 'vue-router';
import root from './root';  // 路由定义

import { ADMIN_USER_TOKEN, USER_TOKEN } from '/@/store/constants'  // Token常量

// 路由权限白名单（无需登录即可访问的页面）
const allowList = ['adminLogin', 'login', 'register', 'portal', 'search', 'detail', '403', '404']
// 前台用户登录地址
const loginRoutePath = '/index/login'
// 后台管理员登录地址
const adminLoginRoutePath = '/adminLogin'


const router = createRouter({
  history: createWebHistory(),
  routes: root,
});

// ==================== 路由守卫 ====================
// 路由跳转前的权限检查
router.beforeEach(async (to, from, next) => {
  console.log(to, from)

  /** 后台管理路由 **/
  if (to.path.startsWith('/admin')) {
    // 检查是否有后台管理Token
    if (localStorage.getItem(ADMIN_USER_TOKEN)) {
      // 已登录，如果访问登录页则跳转到首页
      if (to.path === adminLoginRoutePath) {
        next({ path: '/' })
      } else {
        // 允许访问
        next()
      }
    } else {
      // 未登录
      if (allowList.includes(to.name as string)) {
        // 在免登录白名单，直接进入
        next()
      } else {
        // 跳转到登录页，并记录重定向路径
        next({ path: adminLoginRoutePath, query: { redirect: to.fullPath } })
      }
    }
  }

  /** 前台用户路由 **/
  if (to.path.startsWith('/index')) {
    // 检查是否有前台用户Token
    if (localStorage.getItem(USER_TOKEN)) {
      // 已登录，如果访问登录页则跳转到首页
      if (to.path === loginRoutePath) {
        next({ path: '/' })
      } else {
        // 允许访问
        next()
      }
    } else {
      // 未登录
      if (allowList.includes(to.name as string)) {
        // 在免登录白名单，直接进入
        next()
      } else {
        // 跳转到登录页，并记录重定向路径
        next({ path: loginRoutePath, query: { redirect: to.fullPath } })
      }
    }
  }

});

// ==================== 路由后置守卫 ====================
// 路由跳转后执行
router.afterEach((_to) => {
  // 页面切换后滚动到顶部
  document.getElementById("html")?.scrollTo(0, 0)
});

export default router;
