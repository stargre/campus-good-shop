import { UserConfig, ConfigEnv } from 'vite';
import { createVitePlugins } from './build/vite/plugins';
import { resolve } from 'path';
import { VITE_PORT } from './build/constant';

function pathResolve(dir: string) {
  return resolve(process.cwd(), '.', dir);
}

// https://vitejs.dev/config/
export default ({ command }: ConfigEnv): UserConfig => {
  const isBuild = command === 'build';
  let base: string;
  if (command === 'build') {
    base = '/';
  } else {
    base = '/';
  }
  return {
    base,
    publicDir: "public", //静态资源服务的文件夹
    resolve: {
      alias: [
        {
          find: 'vue-i18n',
          replacement: 'vue-i18n/dist/vue-i18n.cjs.js',
        },
        // 别名 /@/xxxx => src/xxxx
        {
          find: '/@',
          replacement: pathResolve('src') + '/',
        },
      ],
    },
    // plugins
    plugins: createVitePlugins(isBuild),

    css: {
      preprocessorOptions: {
        less: {
          javascriptEnabled: true,
          modifyVars: {
            'primary-color': '#3B82F6',
            'link-color': '#3B82F6',
            'success-color': '#22c55e',
            'warning-color': '#f59e0b',
            'error-color': '#ef4444',
            'heading-color': '#0F172A',
            'text-color': '#111827',
            'text-color-secondary': '#6B7280',
            'border-color-base': '#E5E7EB',
            'component-background': '#FFFFFF',
            'layout-body-background': '#F7F8FA',
            'border-radius-base': '10px',
            'font-size-base': '14px',
            'box-shadow-base': '0 8px 24px rgba(0,0,0,0.07)'
          }
        }
      }
    },

    // server
    server: {
      hmr: { overlay: false }, // 禁用或配置 HMR 连接 设置 server.hmr.overlay 为 false 可以禁用服务器错误遮罩层
      // 服务配置
      port: VITE_PORT, // 类型： number 指定服务器端口;
      open: false, // 类型： boolean | string在服务器启动时自动在浏览器中打开应用程序；
      cors: true, // 类型： boolean | CorsOptions 为开发服务器配置 CORS。默认启用并允许任何源
      host: '0.0.0.0', // IP配置，支持从IP启动
      https: false, // 禁用https
      // proxy,
    },
  };
};
