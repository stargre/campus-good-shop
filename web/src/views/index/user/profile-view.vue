<template>
  <div class="content-list">
    <div class="list-title">个人资料</div>
    <a-spin :spinning="loading" style="min-height: 200px;">
      <div class="list-content">
        <div class="profile-view">
          <div class="item flex-view">
            <div class="label">头像</div>
            <div class="right-box avatar-box flex-view">
              <img v-if="profile.avatar" :src="profile.avatar" class="avatar">
              <img v-else :src="AvatarImg" class="avatar">
              <div class="change-tips flex-view">
                <a-upload name="file" accept="image/*" :multiple="false" :before-upload="beforeUpload">
                  <label>点击更换头像</label>
                </a-upload>
                <p class="tip">图片支持 GIF、PNG、JPEG，尺寸≥200px，大小≤4MB</p>
              </div>
            </div>
          </div>
          <div class="item flex-view">
            <div class="label">昵称</div>
            <div class="right-box">
              <input class="input-dom" v-model="profile.nick" placeholder="请输入昵称" aria-label="昵称" />
            </div>
          </div>
        <div class="item flex-view">
          <div class="label">邮箱</div>
          <div class="right-box">
            <input class="input-dom" v-model="profile.email" placeholder="请输入邮箱" aria-label="邮箱" />
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">手机号</div>
          <div class="right-box">
            <input class="input-dom" v-model="profile.mobile" placeholder="请输入手机号" aria-label="手机号" />
          </div>
        </div>
          <div class="item flex-view">
            <div class="label">学院</div>
            <div class="right-box">
              <input class="input-dom" v-model="profile.collage" placeholder="请输入学院" aria-label="学院" />
            </div>
          </div>
          <div class="item flex-view">
            <div class="label"></div>
            <div class="right-box">
              <a-button shape="round" size="large" type="primary" class="cta-btn" @click="handleSave">
                <template #icon><SaveOutlined /></template>
                保存
              </a-button>
            </div>
          </div>
        </div>
      </div>
    </a-spin>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { detailApi, updateUserInfoApi } from '/@/api/index/user'
import { SaveOutlined } from '@ant-design/icons-vue'
import AvatarImg from '/@/assets/images/avatar.jpg'
import { useUserStore } from '/@/store'
import { getImageUrl } from '/@/utils/url'

let loading = ref(false)
let profile = ref({ nick: '', email: '', mobile: '', collage: '', avatar: '', avatarFile: undefined })
const userStore = useUserStore()

onMounted(()=>{
  getProfile()
})

const getProfile =()=> {
  loading.value = true
  detailApi({ id: userStore.user_id }).then(res => {
    const d = res.data || {}
    profile.value.nick = d.user_name ?? d.nickname ?? ''
    profile.value.email = d.user_email ?? d.email ?? ''
    profile.value.mobile = d.user_mobile ?? d.mobile ?? ''
    profile.value.collage = d.user_collage ?? d.collage ?? ''
    if (d.avatar) {
      profile.value.avatar = getImageUrl(String(d.avatar))
    } else {
      profile.value.avatar = ''
    }
    loading.value = false
  }).catch(err => {
    console.log(err)
    loading.value = false
  })
}

const beforeUpload =(file)=> {
  const fileName = new Date().getTime().toString() + '.' + file.type.substring(6)
  const copyFile = new File([file], fileName)
  profile.value.avatarFile = copyFile
  return false
}

const handleSave = () => {
  const formData = new FormData()
  if (profile.value.avatarFile) formData.append('avatar', profile.value.avatarFile)
  if (profile.value.nick) { formData.append('nickname', profile.value.nick); formData.append('user_name', profile.value.nick) }
  if (profile.value.email) { formData.append('email', profile.value.email); formData.append('user_email', profile.value.email) }
  // 始终提交手机号字段（允许用户清空手机号以删除）
  formData.append('mobile', profile.value.mobile || '')
  formData.append('user_mobile', profile.value.mobile || '')
  if (profile.value.collage) { formData.append('collage', profile.value.collage); formData.append('user_collage', profile.value.collage) }
  updateUserInfoApi({}, formData).then(() => {
    message.success('保存成功')
    getProfile()
  }).catch(err => {
    message.error(err.msg || '保存失败')
  })
}
</script>

<style scoped lang="less">
.flex-view { display: flex; }
.content-list { flex: 1; }
.list-title { color: #152844; font-weight: 600; font-size: 18px; height: 48px; margin-bottom: 4px; border-bottom: 1px solid #cedce4; }
.item { align-items: center; margin: 24px 0; }
.label { width: 100px; color: #152844; font-weight: 600; font-size: 14px; }
.input-dom { background: #f8fafb; border-radius: 4px; width: 240px; height: 40px; line-height: 40px; font-size: 14px; color: #5f77a6; padding: 0 12px; margin-right: 16px; border: 1px solid #d9d9d9; }
.input-dom:focus { border-color: #3B82F6; background: #fff; }
.avatar { width: 48px; height: 48px; border-radius: 50%; margin-right: 16px; }
.avatar-box { align-items: center; gap: 12px; }
.intro { width: 100%; height: 120px; background: #f8fafb; padding: 8px 12px; line-height: 22px; font-size: 14px; color: #152844; resize: none; border: 1px solid #d9d9d9; }
.intro:focus { border-color: #3B82F6; background: #fff; }
.input-dom { border: 1px solid #d9d9d9; }
.input-dom:focus { border-color: #3B82F6; background: #fff; }
.avatar-box { align-items: center; gap: 12px; }
.avatar { width: 48px; height: 48px; border-radius: 50%; margin-right: 16px; }
.intro { width: 100%; height: 120px; background: #f8fafb; padding: 8px 12px; line-height: 22px; font-size: 14px; color: #152844; resize: none; }
</style>
