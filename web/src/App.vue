<template>
  <!-- Ant Design Vue配置提供者，设置中文语言包 -->
  <a-config-provider :locale="zhCN">
    <!-- 路由视图 -->
    <router-view />
  </a-config-provider>
</template>
<script setup lang="ts">
/**
 * 根组件
 * 配置Ant Design Vue的全局语言包，提供路由视图容器
 */

import zhCN from 'ant-design-vue/es/locale/zh_CN';  // Ant Design Vue中文语言包

</script>

<style>
/**
 * 应用根样式
 */
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  height: 100vh;  /* 全屏高度 */
}
</style>
