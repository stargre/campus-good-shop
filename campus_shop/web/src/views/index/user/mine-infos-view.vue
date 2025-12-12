<template>
  <div class="mine-infos-view">
    <div class="info-box flex-view">
      <img :src="avatarUrl || AvatarImg" class="avatar-img" alt="用户头像">
      <div class="name-box">
        <h2 class="nick">{{ userStore.user_name }}</h2>
        <div class="age">
          <span>活跃1天</span>
          <span class="give-point"></span>
        </div>
      </div>
    </div>
    <div class="counts-view">
      <div class="counts flex-view">
        <div class="fans-box flex-item" @click="clickMenu('collectProductView')">
          <div class="text">收藏</div>
          <div class="num">{{collectCount}}</div>
        </div>
        <div class="split-line">
        </div>
        
<!--        <div class="split-line">-->
<!--        </div>-->
<!--        <div class="points-box flex-item">-->
<!--          <div class="text">积分</div>-->
<!--          <div class="num">0</div>-->
<!--        </div>-->
      </div>
    </div>
    <div class="order-box">
      <div class="title">订单中心</div>
      <div class="list">
        <div class="mine-item flex-view" @click="clickMenu('orderView')">
          <ProfileOutlined class="menu-icon" />
          <span>我的订单</span>
        </div>
        <div class="mine-item flex-view" @click="clickMenu('commentView')">
          <MessageOutlined class="menu-icon" />
          <span>我的评论</span>
        </div>
        <div class="mine-item flex-view" @click="clickMenu('addressView')">
          <EnvironmentOutlined class="menu-icon" />
          <span>地址管理</span>
        </div>
        
      </div>
    </div>
    <div class="product-box">
      <div class="title">商品管理</div>
      <div class="list">
        <div class="mine-item flex-view" @click="clickMenu('productList')">
          <ShoppingOutlined class="menu-icon" />
          <span>我的商品</span>
        </div>
      </div>
    </div>
    <div class="setting-box">
      <div class="title">个人设置</div>
        <div class="list">
        <div class="mine-item flex-view" @click="clickMenu('securityView')">
          <SafetyOutlined class="menu-icon" />
          <span>账号安全</span>
        </div>
        
        <div class="mine-item flex-view" @click="clickMenu('profileView')">
          <IdcardOutlined class="menu-icon" />
          <span>个人资料</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AvatarImg from '/@/assets/images/avatar.jpg'
import { getImageUrl } from '/@/utils/url'
import { detailApi } from '/@/api/index/user'
import { ProfileOutlined, MessageOutlined, EnvironmentOutlined, ShoppingOutlined, SettingOutlined, SafetyOutlined, IdcardOutlined } from '@ant-design/icons-vue'

import {getProductCollectListApi} from '/@/api/index/product'
import {useUserStore} from '/@/store';
const userStore = useUserStore();
const avatarUrl = ref('');
const router = useRouter();


let collectCount = ref(0)

onMounted(()=>{
  getCollectProductList()
  loadAvatar()
})

const clickMenu =(name)=> {
  router.push({name: name})
}
const getCollectProductList =()=> {
  let username = userStore.user_name
  getProductCollectListApi({username: username}).then(res => {
    collectCount.value = res.data.length
  }).catch(err => {
    console.log(err.msg)
  })
}

const loadAvatar = async () => {
  if (!userStore.user_id) {
    avatarUrl.value = ''
    return
  }
  try {
    const res = await detailApi({ id: userStore.user_id })
    avatarUrl.value = getImageUrl(res.data?.avatar || res.data?.user_avart || '')
  } catch (_) {
    avatarUrl.value = ''
  }
}



</script>

<style scoped>
.flex-view { display: flex; }
.mine-infos-view { width: 235px; margin-right: 20px; border: 1px solid #cedce4; height: fit-content; }
.mine-infos-view .info-box { align-items: center; padding: 16px 16px 0; overflow: hidden; }
.mine-infos-view .avatar-img { width: 48px; height: 48px; margin-right: 16px; border-radius: 50%; }
.mine-infos-view .name-box { flex: 1; overflow: hidden; }
.mine-infos-view .name-box .nick { color: #152844; font-weight: 600; font-size: 18px; line-height: 24px; height: 24px; text-overflow: ellipsis; white-space: nowrap; margin: 0; overflow: hidden; }
.mine-infos-view .name-box .age { font-size: 12px; color: #6f6f6f; height: 16px; line-height: 16px; margin-top: 8px; }
.mine-infos-view .name-box .give-point { color: #4684e2; cursor: pointer; float: right; }
.mine-infos-view .counts-view { border: none; padding: 16px; }
.mine-infos-view .counts { margin-top: 12px; text-align: center; align-items: center; }
.mine-infos-view .counts .flex-item { flex: 1; cursor: pointer; border-radius: 8px; transition: transform .08s ease, box-shadow .16s ease, background-color .2s ease; padding: 8px 0; }
.mine-infos-view .counts .flex-item:hover { transform: translateY(-1px); box-shadow: 0 8px 18px rgba(0,0,0,0.08); background: #f9fafb; }
.mine-infos-view .counts .flex-item:active { transform: scale(0.98); box-shadow: inset 0 2px 8px rgba(0,0,0,0.12); }
.mine-infos-view .counts .text { height: 16px; line-height: 16px; color: #6f6f6f; }
.mine-infos-view .counts .num { height: 18px; line-height: 18px; color: #152844; font-weight: 600; font-size: 14px; margin-top: 4px; }
.mine-infos-view .counts .split-line { width: 1px; height: 24px; background: #dae6f9; }
.mine-infos-view .order-box, .mine-infos-view .product-box, .mine-infos-view .setting-box { border-top: 1px solid #cedce4; padding: 16px; }
.mine-infos-view .title { color: #152844; font-weight: 600; font-size: 14px; line-height: 18px; height: 18px; margin-bottom: 8px; }
.mine-infos-view .list { padding-left: 16px; }
.mine-infos-view .mine-item { border-top: 1px dashed #cedce4; cursor: pointer; height: 48px; align-items: center; border-radius: 8px; transition: transform .08s ease, box-shadow .16s ease, background-color .2s ease; padding: 0 8px; display: flex; }
.mine-infos-view .mine-item:hover { transform: translateY(-1px); box-shadow: 0 8px 18px rgba(0,0,0,0.08); background: #f9fafb; }
.mine-infos-view .mine-item:active { transform: scale(0.98); box-shadow: inset 0 2px 8px rgba(0,0,0,0.12); }
.mine-infos-view .mine-item:first-child { border: none; }
.mine-infos-view .mine-item .menu-icon { font-size: 20px; width: 20px; height: 20px; line-height: 20px; margin-right: 8px; color: #6B7280; }
.mine-infos-view .mine-item img { width: 20px; height: 20px; margin-right: 8px; }
.mine-infos-view .mine-item span { color: #152844; font-size: 14px; }
</style>
