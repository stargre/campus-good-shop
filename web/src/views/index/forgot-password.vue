<template>
  <div class="container">
    <div class="page-box">
      <h2>找回密码</h2>
      <div class="form-item">
        <input v-model="email" placeholder="请输入注册邮箱" />
      </div>
      <div class="form-item">
        <button @click="submit" :disabled="sending">发送重置邮件</button>
      </div>
      <div class="form-item" v-if="sent">
        <input v-model="code" placeholder="请输入控制台验证码" />
        <button @click="verify" :disabled="verifying">验证验证码</button>
      </div>
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { message as antdMessage } from 'ant-design-vue'
import { passwordResetRequestApi, passwordResetVerifyApi } from '/@/api/index/user'
import { useRouter } from 'vue-router'

const email = ref('')
const code = ref('')
const sent = ref(false)
const sending = ref(false)
const verifying = ref(false)
const message = ref('')
const router = useRouter()

const submit = async () => {
  if (!email.value) {
    antdMessage.warn('请填写邮箱')
    return
  }
  sending.value = true
  try {
    await passwordResetRequestApi({ email: email.value })
    sent.value = true
    message.value = '验证码已发送（查看服务器控制台或邮箱），请输入验证码进行验证'
    antdMessage.success('验证码已发送（查看服务器控制台）')
  } catch (e: any) {
    antdMessage.error(e?.msg || '发送失败')
  } finally {
    sending.value = false
  }
}

const verify = async () => {
  if (!email.value || !code.value) {
    antdMessage.warn('请填写邮箱与验证码')
    return
  }
  verifying.value = true
  try {
    console.log('验证提交', { email: email.value, code: code.value })
    const res = await passwordResetVerifyApi({ email: email.value, code: code.value })
    console.log('验证响应', res)
    // 成功后跳转到重置页面，携带 token
    const token = res.data?.token || res?.token || ''
    if (token) {
      antdMessage.success('验证通过，跳转到重置密码页面')
      router.push({ name: 'resetPassword', query: { token } })
    } else {
      // 如果返回没有 token ，也提示成功以兼容
      antdMessage.success('验证通过，跳转到重置密码页面')
      router.push({ name: 'resetPassword' })
    }
  } catch (e: any) {
    console.error('验证失败异常', e)
    antdMessage.error(e?.msg || '验证失败')
  } finally {
    verifying.value = false
  }
}
</script>

<style scoped>
.container { display:flex; justify-content:center; padding: 40px 0 }
.page-box { width: 360px; background: #fff; padding: 24px; border-radius:6px }
.form-item { margin-bottom: 12px }
input { width:100%; height:36px; padding:6px 8px }
button { width:100%; height:36px; background:#3d5b96; color:#fff; border:none }
</style>
