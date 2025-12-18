<template>
  <div class="content-list">
    <div class="list-title">发布闲置物品</div>
    <div class="publish-form">
      <div class="item flex-view">
        <div class="label required">商品标题</div>
        <div class="right-box">
          <input type="text" class="input-dom" placeholder="请输入商品标题" v-model="formData.product_title">
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
        <div class="label required">商品原价</div>
        <div class="right-box">
          <span class="price-prefix">¥</span>
          <input type="number" class="input-dom price-input" placeholder="0.00" v-model="formData.product_o_price">
        </div>
      </div>
      
      <div class="item flex-view">
        <div class="label required">商品现价</div>
        <div class="right-box">
          <span class="price-prefix">¥</span>
          <input type="number" class="input-dom price-input" placeholder="0.00" v-model="formData.product_price">
        </div>
      </div>
      
      <div class="item flex-view">
        <div class="label required">商品成色</div>
        <div class="right-box">
          <a-select 
            v-model:value="formData.quality" 
            placeholder="请选择商品成色" 
            class="select-dom"
          >
            <a-select-option value="1">全新</a-select-option>
            <a-select-option value="2">几乎全新</a-select-option>
            <a-select-option value="3">轻微使用痕迹</a-select-option>
            <a-select-option value="4">明显使用痕迹</a-select-option>
          </a-select>
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
            v-model="formData.content"
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
        <a-button shape="round" size="large" class="cta-btn ghost" @click="handleCancel">
          <template #icon><RollbackOutlined /></template>
          取消
        </a-button>
        <a-button shape="round" size="large" type="primary" class="cta-btn" @click="handleSubmit">
          <template #icon><CloudUploadOutlined /></template>
          发布
        </a-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { PlusOutlined, UploadOutlined, RollbackOutlined, CloudUploadOutlined } from '@ant-design/icons-vue'
import { getCategoryList } from '/@/api/index/category'
import { createProduct } from '/@/api/index/product'
import { uploadImageApi } from '/@/api/index/upload'
import { useUserStore } from '/@/store'

const router = useRouter()
const userStore = useUserStore()

// 表单数据
const formData = ref({
  product_title: '',
  category_id: '',
  product_o_price: '',
  product_price: '',
  quality: '',
  content: '',
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
  // 检查图片数量限制（仅允许一张）
  if (fileList.value.length >= 1) {
    message.error('只能上传一张图片')
    return false
  }
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
  // 重要：返回false会阻止文件被添加到fileList，导致customRequest不被调用
  // 我们需要返回true让Ant Design Upload将文件添加到fileList，然后自定义上传会处理
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
    // 注意：file.uid来自上传器，需要在fileList中找到对应的项
    const uid = file.uid
    console.log('开始查找fileList中uid为', uid, '的项, 当前fileList长度:', fileList.value.length)
    
    const idx = fileList.value.findIndex(it => {
      console.log('比较 it.uid:', it.uid, '(类型:', typeof it.uid, ') vs uid:', uid, '(类型:', typeof uid, ')')
      return String(it.uid) === String(uid)
    })
    
    console.log('找到的索引:', idx)
    
    if (idx !== -1) {
      // 更新文件对象的属性
      const fileObj = fileList.value[idx]
      fileObj.url = url
      fileObj.status = 'done'
      // 触发响应式更新，确保后续读取到最新url
      fileList.value = [...fileList.value]
      console.log('文件列表更新成功，索引:', idx, '文件对象:', fileObj)
    } else {
      console.warn('未找到对应的fileList项!')
    }
    
    // 调用成功回调
    onSuccess && onSuccess({ url })
  } catch (e) {
    console.error('图片上传失败:', e)
    onError && onError(e)
    message.error('图片上传失败: ' + (e.message || '未知错误'))
  }
}

// 表单验证
const validateForm = () => {
  if (!formData.value.product_title) {
    message.error('请输入商品标题')
    return false
  }
  if (!formData.value.category_id) {
    message.error('请选择商品分类')
    return false
  }
  if (!formData.value.product_o_price || formData.value.product_o_price <= 0) {
    message.error('请输入正确的商品原价')
    return false
  }
  if (!formData.value.product_price || formData.value.product_price <= 0) {
    message.error('请输入正确的商品现价')
    return false
  }
  if (!formData.value.quality) {
    message.error('请选择商品成色')
    return false
  }
  if (fileList.value.length === 0) {
    message.error('请上传至少一张商品图片')
    return false
  }
  if (!formData.value.content) {
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
  
  // 获取上传的图片URL列表
  const uploadedImages = fileList.value
    .map(file => file.url || file.response?.url || file.response?.data?.url)
    .filter(Boolean)
  
  console.log('准备提交的图片列表:', uploadedImages)
  
  if (uploadedImages.length === 0) {
    message.error('请先上传商品图片')
    return
  }
  
  // 准备提交数据
  const submitData = {
    product_title: formData.value.product_title,
    category_id: formData.value.category_id,
    product_price: formData.value.product_price,
    product_o_price: formData.value.product_o_price,
    quality: formData.value.quality,
    content: formData.value.content,
    location: formData.value.location,
    contact_info: formData.value.contact_info,
    images: uploadedImages,
    // 设置默认状态为发布，确保首页能展示
    product_status: 1
  }
  
  console.log('提交数据:', submitData)
  
  try {
    const res = await createProduct(submitData)
    console.log('发布响应:', res)
    if (res.data) {
      message.success('发布成功')
      const pid = res.data.product_id || res.data.id
      if (pid) {
        router.push({ name: 'detail', query: { id: String(pid) } })
      } else {
        router.push({ name: 'productList' })
      }
    }
  } catch (err) {
    console.error('发布失败:', err)
    message.error('发布失败: ' + (err.message || '请重试'))
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
