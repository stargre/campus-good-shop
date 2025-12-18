<template>
  <div class="main-bar-view">
    <div class="logo">
      <img src="/favicon.svg" class="logo-icon" alt="校园闲置物品交易平台" @click="$router.push({name:'portal'})">
    </div>
    <div class="search-entry">
      <SearchOutlined class="search-icon" />
      <input placeholder="输入关键词" ref="keywordRef" @keyup.enter="search"/>
    </div>
    <div class="notice-tab">
      <a-button type="link" @click="openNotice">公告</a-button>
    </div>
    <div class="right-view">
      <a href="/admin" target="__black" class="admin-link">后台入口</a>
      <button class="login btn hidden-sm" style="margin-right:12px;" @click="goPublish()">发布商品</button>
      <template v-if="userStore.user_token">
        <a-dropdown>
          <a class="ant-dropdown-link" @click="e => e.preventDefault()">
            <img :src="userAvatar || AvatarIcon" class="self-img">
          </a>
          <template #overlay>
            <a-menu>
              <a-menu-item>
                <a @click="goUserCenter('orderView')">订单中心</a>
              </a-menu-item>
              <a-menu-item>
                <a @click="goUserCenter('userInfoEditView')">个人设置</a>
              </a-menu-item>
              <a-menu-item>
                <a @click="quit()">退出</a>
              </a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
        <!--        <div class="right-icon">-->
        <!--          <img src="@/assets/cart-icon.svg">-->
        <!--          <span>3</span>-->
        <!--        </div>-->
      </template>
      <template v-else>
        <button class="login btn hidden-sm" @click="goLogin()">登录</button>
      </template>

    </div>
  </div>
  <a-modal v-model:visible="noticeVisible" title="平台公告" :footer="null">
    <div style="min-height:80px;white-space:pre-line;">{{ currentNotice }}</div>
    <div style="margin-top:12px;text-align:right;">
      <a-button type="primary" @click="nextNotice">下一条</a-button>
    </div>
  </a-modal>
</template>

<script setup lang="ts">
import { ref, watchEffect, onMounted } from 'vue'
import {listApi} from '/@/api/index/notice'
import {useUserStore} from "/@/store";
import { detailApi as userDetailApi } from '/@/api/index/user'
import AvatarIcon from '/@/assets/images/avatar.jpg';
import { getImageUrl } from '/@/utils/url';
import { SearchOutlined, DeleteOutlined } from '@ant-design/icons-vue';
import {USER_TOKEN} from "/@/store/constants";


const router = useRouter();
const route = useRoute();
const userStore = useUserStore();
const userAvatar = ref('');

const keywordRef = ref()


const search = () => {
  const keyword = keywordRef.value.value
  if (route.name === 'search') {
    router.push({name: 'search', query: {keyword: keyword}})
  } else {
    let text = router.resolve({name: 'search', query: {keyword: keyword}})
    window.open(text.href, '_blank')
  }
}
const goLogin = () => {
  router.push({name: 'login'})
}


const goUserCenter = (menuName) => {
  router.push({name: menuName})
}
const quit = () => {
  userStore.logout().then(res => {
    router.push({name: 'portal'})
  })
}


const goPublish = () => {
  if (userStore.user_token) {
    router.push({ name: 'productPublish' })
  } else {
    router.push({ name: 'login' })
  }
}

// 公告弹窗
const noticeVisible = ref(false)
const notices = ref<string[]>([])
const noticeIndex = ref(0)
const currentNotice = ref('')

const loadNotices = async () => {
  try {
    const res: any = await listApi()
    const list = Array.isArray(res.data) ? res.data : []
    notices.value = list.map((n: any) => String(n.notice_content || ''))
    noticeIndex.value = 0
    currentNotice.value = notices.value[0] || '暂无公告'
  } catch (e) {
    notices.value = []
    currentNotice.value = '暂无公告'
  }
}

const openNotice = async () => {
  if (!notices.value.length) {
    await loadNotices()
  }
  noticeVisible.value = true
}

const nextNotice = () => {
  if (!notices.value.length) return
  noticeIndex.value = (noticeIndex.value + 1) % notices.value.length
  currentNotice.value = notices.value[noticeIndex.value]
}
</script>

<style scoped lang="less">
.main-bar-view {
  position: fixed;
  top: 0;
  left: 0;
  height: 56px;
  width: 100%;
  background: #fff;
  border-bottom: 1px solid #cedce4;
  padding-left: 48px;
  z-index: 16;
  display: flex;
  flex-direction: row;
  //justify-content: center; /*水平居中*/
  align-items: center; /*垂直居中*/
}

.logo {
  margin-right: 24px;

  img {
    width: 32px;
    height: 32px;
    cursor: pointer;
  }
}
 .logo-icon {
   width: 32px;
   height: 32px;
 }

.search-entry {
  position: relative;
  width: 400px;
  min-width: 200px;
  height: 32px;
  background: #ecf3fc;
  padding: 0 12px;
  border-radius: 16px;
  font-size: 0;
  cursor: pointer;
  transition: box-shadow .16s ease;

  img {
    max-width: 100%;
    height: auto;
  }

  .search-icon {
    font-size: 18px;
    margin: 7px 8px 0 0;
  }

  input {
    position: absolute;
    top: 4px;
    width: 85%;
    height: 24px;
    border: 0px;
    outline: none;
    color: #000;
    background: #ecf3fc;
    font-size: 14px;
  }
}

.right-view {
  padding-right: 36px;
  flex: 1;
  display: flex;
  flex-direction: row;
  gap: 20px;
  justify-content: flex-end; /* 内容右对齐 */

  .username {
    height: 32px;
    line-height: 32px;
    text-align: center;
  }

  button {
    outline: none;
    border: none;
    cursor: pointer;
  }

  img {
    cursor: pointer;
  }

  .right-icon {
    position: relative;
    width: 36px;
    height: 36px;
    margin: 4px 0 0 4px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0;
    transition: transform .12s ease, box-shadow .16s ease;
    &:hover { transform: translateY(-1px); }
  
    span {
      position: absolute;
      right: -8px;
      top: -8px;
      font-size: 12px;
      color: #fff;
      background: #4684e2;
      border-radius: 8px;
      padding: 0 4px;
      height: 16px;
      line-height: 16px;
      font-weight: 600;
      min-width: 20px;
      text-align: center;
    }

    .msg-point {
      position: absolute;
      right: -8px;
      top: -8px;
      min-width: 8px;
      width: 14px;
      height: 14px;
      background: #4684e2;
      border-radius: 50%;
    }
  }

  .self-img {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    vertical-align: middle;
    cursor: pointer;
  }

  .btn {
    background: #4684e2;
    font-size: 14px;
    color: #fff;
    border-radius: 32px;
    text-align: center;
    width: 66px;
    height: 32px;
    line-height: 32px;
    vertical-align: middle;
    margin-left: 32px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    transition: transform .08s ease, box-shadow .16s ease;
  }
  .btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.10);
  }
  .delete-icon {
    font-size: 24px;
    margin-left: 4px;
    margin-top: 4px;
    cursor: pointer;
    color: #ff4d4f;
  }
  .cart-icon {
    font-size: 36px;
    line-height: 36px;
  }
  .admin-link {
    line-height: 32px;
    display: inline-block;
    padding: 0 10px;
    border-radius: 20px;
    transition: transform .08s ease, box-shadow .16s ease, background-color .2s ease;
  }
  .admin-link:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.10);
    background: #f3f4f6;
  }
  .admin-link:active {
    transform: scale(0.98);
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.12);
  }
}

.content-list {
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    //line-height: 24px;
    height: 48px;
    margin-bottom: 4px;
    border-bottom: 1px solid #cedce4;
  }
}

.notification-item {
  padding-top: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e9e9e9;

  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin-right: 8px;
  }

  .content-box {
    //border-bottom: 1px dashed #e9e9e9;
    //padding: 4px 0 16px;
    display: flex;
    flex-direction: row;
  }

  .header {
    margin-bottom: 12px;
  }

  .title-txt {
    color: #315c9e;
    font-weight: 500;
    font-size: 14px;
  }

  .time {
    color: #a1adc5;
    font-size: 14px;
  }

  .head-text {
    color: #152844;
    font-weight: 500;
    font-size: 14px;
    line-height: 22px;

    .name {
      margin-right: 8px;
    }
  }

  .content {
    margin-top: 2px;
    flex: 1;
    font-size: 16px;
  }

}

.notice-tab {
  margin: 0 12px;
}

</style>
