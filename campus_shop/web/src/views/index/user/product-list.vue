<template>
  <div class="content-list">
    <div class="list-title flex-view justify-between items-center">
      <span>我的商品</span>
      <button class="publish-btn" @click="handlePublish">发布商品</button>
    </div>
    <div class="product-list">
      <div class="filter-bar flex-view justify-between items-center mb-20">
        <div class="status-filter">
          <a-radio-group v-model:value="statusFilter"
            button-style="solid"
          >
            <a-radio-button value="">全部</a-radio-button>
            <a-radio-button value="1">在售中</a-radio-button>
            <a-radio-button value="0">已售出</a-radio-button>
          </a-radio-group>
        </div>
        <div class="search-box">
          <a-input-search
            placeholder="搜索我的商品"
            v-model:value="searchKeyword"
            allow-clear
            enter-button
            size="middle"
            @search="handleSearch"
          />
        </div>
      </div>
      <div v-if="loading">
        <a-spin tip="加载中...">
          <div class="demo-loading-container"></div>
        </a-spin>
      </div>
      <div v-else-if="productList.length === 0">
        <div class="empty-state">
          <img src="/empty.png" alt="暂无商品">
          <p>还没有发布商品，快去发布吧！</p>
        </div>
      </div>
      <div v-else class="list-content">
        <a-card
          v-for="product in productList"
          :key="product.id"
          hoverable
          class="product-card"
        >
          <div class="card-content flex-view">
            <div class="product-image">
              <img :src="product.cover_image" :alt="product.title" class="image">
              <span v-if="product.status === 0" class="sold-tag">已售出</span>
            </div>
            <div class="product-info flex-1">
              <div class="product-title">{{ product.title }}</div>
              <div class="product-meta flex-view justify-between items-center mb-10">
                <div class="category">{{ getCategoryName(product.category_id) }}</div>
                <div class="price">¥{{ product.price }}</div>
              </div>
              <div class="product-location"><EnvironmentOutlined /> {{ product.location }}</div>
              <div class="product-time">发布时间：{{ formatTime(product.created_at) }}</div>
              <div class="action-buttons flex-view justify-end mt-20">
                <a-button type="primary" @click="handleEdit(product)">编辑<a-button>
                <a-button @click="handleView(product)">查看详情<a-button>
                <a-button type="default" danger @click="handleDelete(product.id)">删除<a-button>
                <div v-if="product.status === 1">
                  <a-button type="default" @click="handleMarkSold(product.id)">标记已售出<a-button>
                </div>
              </div>
            </div>
          </div>
        </a-card>
      </div>
      <div v-if="productList.length > 0" class="pagination-container">
        <a-pagination
          v-model:current="currentPage"
          v-model:pageSize="pageSize"
          :total="total"
          showSizeChanger
          showQuickJumper
          showTotal="(total) => `共 ${total} 条`"
          @change="handlePageChange"
          @showSizeChange="handlePageSizeChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { message, Modal } from 'ant-design-vue'
import { EnvironmentOutlined } from '@ant-design/icons-vue'
import { getMyProductList, deleteProduct, updateProduct } from '/@/api/index/product'
import { getCategoryList } from '/@/api/index/category'

const router = useRouter()

// 状态管理
const loading = ref(false)
const productList = ref([])
const categoryList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const statusFilter = ref('')
const searchKeyword = ref('')

// 初始化
onMounted(() => {
  loadCategoryList()
  loadProductList()
})

// 加载分类列表
const loadCategoryList = () => {
  getCategoryList().then(res => {
    if (res.data) {
      categoryList.value = res.data
    }
  }).catch(err => {
    console.error('加载分类失败:', err)
  })
}

// 加载商品列表
const loadProductList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      status: statusFilter.value || undefined,
      keyword: searchKeyword.value || undefined
    }
    const res = await getMyProductList(params)
    if (res.data) {
      productList.value = res.data.items
      total.value = res.data.total
    }
  } catch (err) {
    console.error('加载商品列表失败:', err)
    message.error('加载商品列表失败')
  } finally {
    loading.value = false
  }
}

// 根据分类ID获取分类名称
const getCategoryName = (categoryId) => {
  const category = categoryList.value.find(cat => cat.id === categoryId)
  return category ? category.name : '未知分类'
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  loadProductList()
}

// 处理状态筛选变化
const handleStatusChange = () => {
  currentPage.value = 1
  loadProductList()
}

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page
  loadProductList()
}

// 处理每页大小变化
const handlePageSizeChange = (current, pageSize) => {
  currentPage.value = current
  pageSize.value = pageSize
  loadProductList()
}

// 发布商品
const handlePublish = () => {
  router.push('/user/product-publish')
}

// 编辑商品
const handleEdit = (product) => {
  router.push({
    path: '/user/product-edit',
    query: { id: product.id }
  })
}

// 查看详情
const handleView = (product) => {
  router.push({
    path: '/detail',
    query: { id: product.id }
  })
}

// 删除商品
const handleDelete = (productId) => {
  Modal.confirm({
    title: '确认删除',
    content: '确定要删除这个商品吗？删除后将无法恢复。',
    okText: '确定',
    cancelText: '取消',
    onOk: async () => {
      try {
        await deleteProduct(productId)
        message.success('删除成功')
        loadProductList()
      } catch (err) {
        console.error('删除失败:', err)
        message.error('删除失败')
      }
    }
  })
}

// 标记为已售出
const handleMarkSold = (productId) => {
  Modal.confirm({
    title: '确认操作',
    content: '确定要将该商品标记为已售出吗？',
    okText: '确定',
    cancelText: '取消',
    onOk: async () => {
      try {
        await updateProduct(productId, { status: 0 })
        message.success('操作成功')
        loadProductList()
      } catch (err) {
        console.error('操作失败:', err)
        message.error('操作失败')
      }
    }
  })
}

// 监听状态筛选变化
const unwatch = watch(statusFilter, handleStatusChange)

// 组件卸载时清理
onUnmounted(() => {
  unwatch()
})
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

    .publish-btn {
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
}

.product-list {
  padding: 0 20px;

  .mb-10 {
    margin-bottom: 10px;
  }

  .mb-20 {
    margin-bottom: 20px;
  }

  .mt-20 {
    margin-top: 20px;
  }

  .filter-bar {
    margin-bottom: 20px;
  }

  .demo-loading-container {
    height: 300px;
  }

  .empty-state {
    text-align: center;
    padding: 60px 0;

    img {
      width: 120px;
      height: 120px;
      margin-bottom: 16px;
    }

    p {
      color: #8c8c8c;
      font-size: 14px;
    }
  }

  .list-content {
    .product-card {
      margin-bottom: 20px;

      .card-content {
        .product-image {
          position: relative;
          width: 160px;
          height: 160px;
          margin-right: 20px;

          .image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 4px;
          }

          .sold-tag {
            position: absolute;
            top: 8px;
            right: 8px;
            background: #ff4d4f;
            color: #fff;
            padding: 2px 8px;
            border-radius: 2px;
            font-size: 12px;
          }
        }

        .product-info {
          .product-title {
            font-size: 16px;
            font-weight: 600;
            color: #152844;
            margin-bottom: 12px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }

          .product-meta {
            .category {
              color: #8c8c8c;
              font-size: 14px;
            }

            .price {
              color: #ff4d4f;
              font-size: 18px;
              font-weight: 600;
            }
          }

          .product-location,
          .product-time {
            color: #8c8c8c;
            font-size: 14px;
            margin-bottom: 8px;
          }

          .action-buttons {
            gap: 12px;
          }
        }
      }
    }
  }

  .pagination-container {
    margin-top: 30px;
    text-align: right;
  }
}

.flex-view {
  display: flex;
}

.justify-between {
  justify-content: space-between;
}

.justify-end {
  justify-content: flex-end;
}

.items-center {
  align-items: center;
}

.flex-1 {
  flex: 1;
}
</style>