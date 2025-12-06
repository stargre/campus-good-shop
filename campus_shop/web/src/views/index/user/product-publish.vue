<template>
  <div class="content-list">
    <div class="list-title">发布二手商品</div>
    <div class="publish-form">
      <div class="item flex-view">
        <div class="label required">商品标题</div>
        <div class="right-box">
          <input type="text" class="input-dom" placeholder="请输入商品标题" v-model="formData.title">
        </div>
      </div>
      
      <div class="item flex-view">
        <div class="label required">商品分类</div>
        <div class="right-box">
          <a-select 
            v-model:value="formData.category_id" 
            placeholder="请选择分类" 
            class="select-dom"
          >
            <a-select-option 
              v-for="category in categoryList" 
              :key="category.id" 
              :value="category.id"
            >
              {{ category.name }}
            </a-select-option>
          </a-select>
        </div>
      </div>
      
      <div class="item flex-view">
        <div class="label required">商品价格</div>
        <div class="right-box">
          <span class="price-prefix">¥</span>
          <input type="number" class="input-dom price-input" placeholder="0.00" v-model="formData.price">
        </div>
      </div>
      
      <div class="item flex-view">
        <div class="label required">商品图片</div>
        <div class="right-box">
          <div class="upload-box">
            <a-upload
              v-model:file-list="fileList"
              list-type="picture-card"
              :before-upload="beforeUpload"
              :custom-request="customRequest"
              :multiple="true"
            >
              <div v-if="fileList.length < 9">
                <PlusOutlined />
                <div style="margin-top: 8px">上传图片</div>
              </div>
            </a-upload>
          </div>
        </div>
      </div>
      
      <div class="item flex-view">
        <div class="label required">商品描述</div>
        <div class="right-box">
          <textarea 
            class="textarea-dom" 
            placeholder="请详细描述商品信息，包括成色、使用情况等" 
            v-model="formData.description"
            rows="6"
          ></textarea>
        </div>
      </div>
      
      <div class="item flex-view">
        <div class="label required">交易地点</div>
        <div class="right-box">
          <input type="text" class="input-dom" placeholder="请输入交易地点" v-model="formData.location">
        </div>
      </div>
      
      <div class="item flex-view">
        <div class="label">联系方式</div>
        <div class="right-box">
          <input type="text" class="input-dom" placeholder="请输入手机号或微信号" v-model="formData.contact_info">
        </div>
      </div>
      
      <div class="submit-btn">
        <button class="cancel" @click="handleCancel">取消</button>
        <button class="save" @click="handleSubmit">发布</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { getCategoryList } from '/@/api/index/category'
import { createProduct } from '/@/api/index/product'
import { useUserStore } from '/@/store'

const router = useRouter()
const userStore = useUserStore()

// 表单数据
const formData = ref({
  title: '',
  category_id: '',
  price: '',
  description: '',
  location: '',
  contact_info: ''
})

// 分类列表
const categoryList = ref([])

// 图片文件列表
const fileList = ref([])

// 上传的图片URL列表
const imageUrls = ref([])

// 初始化
onMounted(() => {
  loadCategoryList()
})

// 加载分类列表
const loadCategoryList = () => {
  getCategoryList().then(res => {
    if (res.data) {
      categoryList.value = res.data
    }
  }).catch(err => {
    console.error('加载分类失败:', err)
    message.error('加载分类失败')
  })
}

// 图片上传前检查
const beforeUpload = (file) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  if (!isJpgOrPng) {
    message.error('只支持JPG和PNG格式的图片!')
    return false
  }
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    message.error('图片大小不能超过2MB!')
    return false
  }
  return false // 阻止默认上传，使用自定义上传
}

// 自定义上传处理
const customRequest = ({ onSuccess }) => {
  // 模拟上传成功，实际项目中这里应该调用上传接口
  setTimeout(() => {
    onSuccess('ok')
  }, 0)
}

// 表单验证
const validateForm = () => {
  if (!formData.value.title) {
    message.error('请输入商品标题')
    return false
  }
  if (!formData.value.category_id) {
    message.error('请选择商品分类')
    return false
  }
  if (!formData.value.price || formData.value.price <= 0) {
    message.error('请输入正确的商品价格')
    return false
  }
  if (fileList.value.length === 0) {
    message.error('请上传至少一张商品图片')
    return false
  }
  if (!formData.value.description) {
    message.error('请输入商品描述')
    return false
  }
  if (!formData.value.location) {
    message.error('请输入交易地点')
    return false
  }
  return true
}

// 提交表单
const handleSubmit = async () => {
  if (!validateForm()) return
  
  // 准备提交数据
  const submitData = {
    ...formData.value,
    image_urls: fileList.value.map(file => file.url || URL.createObjectURL(file.originFileObj))
  }
  
  try {
    const res = await createProduct(submitData)
    if (res.data) {
      message.success('发布成功')
      router.push('/user/product-list')
    }
  } catch (err) {
    console.error('发布失败:', err)
    message.error('发布失败，请重试')
  }
}

// 取消
const handleCancel = () => {
  router.back()
}
</script>

<style scoped lang="less">
.content-list {
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    height: 48px;
    margin-bottom: 24px;
    border-bottom: 1px solid #cedce4;
  }
}

.publish-form {
  padding: 0 20px;

  .item {
    -webkit-box-align: start;
    -ms-flex-align: start;
    align-items: flex-start;
    margin: 24px 0;

    .label {
      width: 100px;
      color: #152844;
      font-weight: 600;
      font-size: 14px;
      margin-top: 8px;
    }

    .required::before {
      content: '*';
      color: #ff4d4f;
      margin-right: 4px;
    }

    .right-box {
      flex: 1;
      margin-left: 20px;
    }

    .input-dom {
      background: #f8fafb;
      border-radius: 4px;
      width: 400px;
      height: 40px;
      line-height: 40px;
      font-size: 14px;
      color: #152844;
      padding: 0 12px;
      border: 1px solid transparent;
      transition: all 0.3s;

      &:focus {
        border-color: #4684e2;
        background: #fff;
      }
    }

    .select-dom {
      width: 400px;
    }

    .textarea-dom {
      background: #f8fafb;
      border-radius: 4px;
      width: 400px;
      font-size: 14px;
      color: #152844;
      padding: 8px 12px;
      border: 1px solid transparent;
      transition: all 0.3s;
      resize: vertical;
      min-height: 100px;

      &:focus {
        border-color: #4684e2;
        background: #fff;
      }
    }

    .price-prefix {
      font-size: 16px;
      color: #152844;
      margin-right: 4px;
      margin-top: 8px;
      display: inline-block;
    }

    .price-input {
      width: 350px;
    }

    .upload-box {
      width: 400px;
    }
  }

  .submit-btn {
    display: flex;
    justify-content: flex-start;
    margin-top: 40px;
    margin-left: 120px;
    gap: 20px;
  }

  .cancel {
    cursor: pointer;
    background: #fff;
    border-radius: 32px;
    width: 96px;
    height: 32px;
    line-height: 32px;
    font-size: 14px;
    color: #152844;
    border: 1px solid #d9d9d9;
    outline: none;
    transition: all 0.3s;

    &:hover {
      color: #4684e2;
      border-color: #4684e2;
    }
  }

  .save {
    cursor: pointer;
    background: #4684e2;
    border-radius: 32px;
    width: 96px;
    height: 32px;
    line-height: 32px;
    font-size: 14px;
    color: #fff;
    border: none;
    outline: none;
    transition: all 0.3s;

    &:hover {
      background: #2c68c7;
    }
  }
}
</style>