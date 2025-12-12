<template>
  <div class="content-list">
    <div class="list-title">编辑闲置物品</div>
    <div v-if="loading">
      <a-spin tip="加载中...">
        <div class="demo-loading-container"></div>
      </a-spin>
    </div>
    <div v-else class="publish-form">
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
              {{ category.name || category.title || category.category_name }}
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
        <div class="label required">商品图片（仅限一张）</div>
        <div class="right-box">
          <div class="upload-box">
            <a-upload
              v-model:file-list="fileList"
              list-type="picture-card"
              :before-upload="beforeUpload"
              :custom-request="customRequest"
              :max-count="1"
              accept="image/jpeg,image/png"
            >
              <div v-if="fileList.length < 1">
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
      
      <div class="item flex-view">
        <div class="label required">商品状态</div>
        <div class="right-box">
          <a-radio-group v-model:value="formData.status" button-style="solid">
            <a-radio-button value="1">在售中</a-radio-button>
            <a-radio-button value="0">已售出</a-radio-button>
          </a-radio-group>
        </div>
      </div>
      
      <div class="submit-btn">
        <a-button shape="round" size="large" class="cta-btn ghost" @click="handleCancel">
          <template #icon><RollbackOutlined /></template>
          取消
        </a-button>
        <a-button shape="round" size="large" type="primary" class="cta-btn" @click="handleSubmit">
          <template #icon><SaveOutlined /></template>
          保存修改
        </a-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { PlusOutlined, UploadOutlined, RollbackOutlined, SaveOutlined } from '@ant-design/icons-vue'
import { getCategoryList } from '/@/api/index/category'
import { getProductDetail, updateProduct } from '/@/api/index/product'
import { uploadImageApi } from '/@/api/index/upload'

const router = useRouter()
const route = useRoute()

// 表单数据
const formData = ref({
  title: '',
  category_id: '',
  price: '',
  description: '',
  location: '',
  contact_info: '',
  status: '1'
})

// 分类列表
const categoryList = ref([])

// 图片文件列表
const fileList = ref([])

// 加载状态
const loading = ref(true)

// 商品ID
const productId = ref('')

// 初始化
onMounted(() => {
  productId.value = String(route.query.id || '')
  if (!productId.value) {
    message.error('商品ID不存在')
    router.back()
    return
  }
  loadCategoryList()
  loadProductDetail()
})

// 加载分类列表
const loadCategoryList = () => {
  getCategoryList().then(res => {
    if (res.data) {
      categoryList.value = res.data.map((c) => ({ id: c.category_id, name: c.category_name }))
    }
  }).catch(err => {
    console.error('加载分类失败:', err)
    message.error('加载分类失败')
  })
}

// 加载商品详情
const loadProductDetail = async () => {
  try {
    const res = await getProductDetail(Number(productId.value))
    if (res.data) {
      const product = res.data
      formData.value = {
        title: product.product_title,
        category_id: product.category,
        price: product.product_price_yuan,
        description: product.content,
        location: product.location,
        contact_info: product.contact_info,
        status: String(product.product_status)
      }
      
      // 设置图片列表
      if (product.images && product.images.length > 0) {
        fileList.value = product.images.map(img => ({
          uid: Date.now() + Math.random().toString(36).substr(2, 9),
          name: (img.image_url||'').split('/').pop() || 'image.jpg',
          status: 'done',
          url: img.image_url
        }))
      }
    }
  } catch (err) {
    console.error('加载商品详情失败:', err)
    message.error('加载商品详情失败')
  } finally {
    loading.value = false
  }
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
  // 返回true让文件被添加到fileList，customRequest会处理上传
  return true
}

// 自定义上传处理
const customRequest = async ({ file, onSuccess, onError }) => {
  try {
    const fd = new FormData()
    fd.append('file', file.originFileObj || file)
    console.log('开始上传图片:', file.name, 'uid:', file.uid)
    const res = await uploadImageApi(fd)
    console.log('上传响应:', res)
    
    // 获取正确的URL路径 - res本身就是APIResponse对象
    // APIResponse结构: { code: 0, msg: '上传成功', data: { url: '/upload/...' } }
    const apiResponse = res
    if (!apiResponse) {
      throw new Error('服务器未返回响应')
    }
    
    let url = ''
    if (apiResponse.code === 0 && apiResponse.data && apiResponse.data.url) {
      // 正确的响应结构
      url = apiResponse.data.url
    } else {
      throw new Error(apiResponse.msg || '上传失败')
    }
    
    if (!url) {
      throw new Error('服务器未返回图片URL')
    }
    
    console.log('图片上传成功，URL:', url)
    
    // 更新文件列表中的URL
    const uid = file.uid
    console.log('开始查找fileList中uid为', uid, '的项, 当前fileList长度:', fileList.value.length)
    
    const idx = fileList.value.findIndex(it => {
      console.log('比较 it.uid:', it.uid, '(类型:', typeof it.uid, ') vs uid:', uid, '(类型:', typeof uid, ')')
      return String(it.uid) === String(uid)
    })
    
    console.log('找到的索引:', idx)
    
    if (idx !== -1) {
      const fileObj = fileList.value[idx]
      fileObj.url = url
      fileObj.status = 'done'
      // 触发响应式更新，确保后续读取到最新url
      fileList.value = [...fileList.value]
      console.log('文件列表更新成功，索引:', idx, '文件对象:', fileObj)
    } else {
      console.warn('未找到对应的fileList项!')
    }
    
    onSuccess && onSuccess({ url })
  } catch (e) {
    console.error('图片上传失败:', e)
    onError && onError(e)
    message.error('图片上传失败: ' + (e.message || '未知错误'))
  }
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
  // 编辑允许无图片（保留原图或稍后上传）
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
    id: productId.value,
    title: formData.value.title,
    category_id: formData.value.category_id,
    price: formData.value.price,
    description: formData.value.description,
    location: formData.value.location,
    contact_info: formData.value.contact_info,
    status: formData.value.status,
    images: JSON.stringify(
      fileList.value
        .map(file => file.url || file.response?.url || file.response?.data?.url)
        .filter(Boolean)
    )
  }
  
  try {
    const res = await updateProduct(Number(productId.value), submitData)
    if (res.data) {
      message.success('保存成功')
      router.back()
    }
  } catch (err) {
    console.error('保存失败:', err)
    message.error('保存失败，请重试')
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
    width: 120px;
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

.demo-loading-container {
  height: 400px;
}

.flex-view {
  display: flex;
}
</style>
