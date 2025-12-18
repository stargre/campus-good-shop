<template>
  <div class="container">
    <div class="page-box">
      <h2>重置密码</h2>
      <div class="form-item" v-if="!hasToken">
        <input v-model="email" placeholder="请输入注册邮箱" />
      </div>
      <div class="form-item" v-if="!hasToken">
        <input v-model="code" placeholder="请输入控制台显示的验证码" />
      </div>
      <div class="form-item">
        <input v-model="password" placeholder="请输入新密码" type="password" />
      </div>
      <div class="form-item">
        <input v-model="repassword" placeholder="请重复新密码" type="password" />
      </div>
      <div class="form-item">
        <button @click="submit">确认重置</button>
      </div>
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { passwordResetConfirmApi } from '/@/api/index/user'
import { message as antdMessage } from 'ant-design-vue'

const route = useRoute()
const router = useRouter()
const token = ref<string | null>(null)
const hasToken = ref(false)
const email = ref('')
const code = ref('')
const password = ref('')
const repassword = ref('')
const message = ref('')

onMounted(() => {
  const q = route.query.token as string | undefined
  if (q) {
    token.value = q
    hasToken.value = true
  }
})

const submit = async () => {
  if (!password.value || !repassword.value) {
    antdMessage.warn('请输入并确认新密码')
    return
  }
  if (password.value !== repassword.value) {
    antdMessage.warn('两次密码不一致')
    return
  }

  const payload: any = { password: password.value, repassword: repassword.value }
  if (hasToken.value && token.value) {
    payload.token = token.value
  } else {
    if (!email.value || !code.value) {
      antdMessage.warn('请填写邮箱与验证码')
      return
    }
    payload.email = email.value
    payload.code = code.value
  }

  try {
    await passwordResetConfirmApi(payload)
    antdMessage.success('密码重置成功，请登录')
    router.push({ name: 'login' })
  } catch (e: any) {
    antdMessage.error(e?.msg || '重置失败')
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
