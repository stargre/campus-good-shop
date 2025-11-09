/**
 * Vue应用入口文件
 * 初始化Vue应用，配置路由、状态管理、UI组件库等
 */
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // 路由配置
import piniaStore from './store';  // 状态管理（Pinia）

import bootstrap from './core/bootstrap';  // 应用启动配置
import '/@/styles/reset.less';  // 样式重置
import '/@/styles/index.less';  // 全局样式
import Antd from 'ant-design-vue';  // Ant Design Vue组件库

// 创建Vue应用实例
const app = createApp(App);

// 注册插件
app.use(Antd);  // 使用Ant Design Vue
app.use(router);  // 使用路由
app.use(piniaStore);  // 使用状态管理
app.use(bootstrap);  // 使用启动配置

// 挂载应用到DOM
app.mount('#app');
