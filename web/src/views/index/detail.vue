<template>
  <div class="detail">
    <Header/>
    <div class="detail-content">
      <div class="product-infos-view flex-view">
        <div class="product-infos">
          <div class="product-img-box">
            <img :src="detailData.cover" :alt="detailData.title" />
          </div>
          <div class="product-info-box">
            <div class="product-state">
              <span class="state" v-if="detailData.status === 1">在售</span>
              <span class="state" v-else>已售出</span>
              <span>{{ detailData.location }}</span>
            </div>
            <div class="product-name">{{ detailData.title }}</div>
            <div class="translators">
              <span>发布时间：{{ detailData.create_time }}</span>
            </div>
            <div class="authors">
              <span>发布者：{{ detailData.user_name }}</span>
            </div>
            <div class="price" style="margin-top: 20px; font-size: 24px; color: #ff7b31;">
              ¥{{ detailData.price }}
            </div>
            <div class="tags" style="position: static; margin-top: 20px;">
              <div class="category-box">
                <span class="title">分类：</span>
                <a-tag color="geekblue">{{ detailData.category_name }}</a-tag>
              </div>
            </div>
            <div style="margin-top: 20px; padding: 12px; background: #f5f5f5; border-radius: 4px;" v-if="detailData.content">
              <div style="font-weight: 600; margin-bottom: 8px; color: #333;">商品简介</div>
              <div style="color: #666; line-height: 1.6; white-space: pre-wrap;">{{ detailData.content }}</div>
            </div>
          </div>
          <div class="product-counts">
            <div class="action-row">
              <a-button
                type="primary"
                size="large"
                shape="round"
                class="cta-btn"
                :disabled="detailData.status !== 1"
                @click="showReserveModal = true"
              >
                <template #icon><CalendarOutlined /></template>
                预约商品
              </a-button>
              <a-button
                size="large"
                shape="round"
                :class="['cta-btn', isFavorited ? 'favored' : 'ghost']"
                @click="handleToggleFavorite"
              >
                <template #icon>
                  <component :is="isFavorited ? HeartFilled : HeartOutlined" />
                </template>
                {{ isFavorited ? '取消收藏' : '加入收藏' }}
              </a-button>
            </div>

            <div class="description-card" v-if="detailData.content || detailData.location || detailData.quality_text">
              <div class="desc-header">
                <div class="desc-title">商品简介</div>
                <div class="desc-meta">
                  <span class="meta-item">地点：{{ detailData.location || '未知地点' }}</span>
                  <span class="meta-item">成色：{{ detailData.quality_text || '未知' }}</span>
                  <span class="meta-item">发布者：{{ detailData.user_name || '匿名' }}</span>
                </div>
              </div>
              <div class="desc-body" v-if="detailData.content">{{ detailData.content }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="comments" style="width:1024px;margin:20px auto;">
      <h3 style="margin-bottom:12px;">评论</h3>
      <div v-if="commentList.length === 0" style="color:#6f6f6f;">暂无评论</div>
      <a-list v-else :data-source="commentList" item-layout="horizontal">
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta :description="item.comment_time">
              <template #title>
                <div class="comment-title">{{ item.buyer_name }}</div>
              </template>
              <template #avatar>
                <a-avatar :src="getImageUrl(item.avatar || item.user_avart || '') || AvatarImg" size="32" />
              </template>
            </a-list-item-meta>
            <div class="comment-content">{{ item.comment_content }}</div>
            <a-button v-if="item.user_id === userStore.user_id" type="link" danger @click="handleDeleteComment(item)">删除</a-button>
          </a-list-item>
        </template>
      </a-list>
      <div style="margin-top:12px;">
        <Input.TextArea v-model:value="commentForm.content" :rows="3" placeholder="写下你的看法" />
        <div style="margin-top:8px;">
          <a-button type="primary" @click="handleCreateComment">发布评论</a-button>
        </div>
      </div>
    </div>
    <Footer/>
    <!-- 预约弹窗 -->
    <a-modal
      v-model:visible="showReserveModal"
      title="预约商品"
      :confirm-loading="reserveLoading"
      @ok="handleReserve"
      @cancel="showReserveModal = false"
    >
      <div class="reserve-form">
        <div class="form-item">
          <label>预约时间：</label>
          <DatePicker
            v-model:value="reserveForm.reserve_time"
            style="width: 100%;"
            placeholder="请选择预约日期"
            format="YYYY-MM-DD"
          />
          <TimePicker
            v-model:value="reserveForm.reserve_time_time"
            style="width: 100%; margin-top: 8px;"
            placeholder="请选择预约时间（可选）"
            format="HH:mm"
          />
        </div>
        <div class="form-item">
          <label>交易地点：</label>
          <Input
            v-model:value="reserveForm.trade_location"
            placeholder="请输入交易地点"
          />
        </div>
        <div class="form-item">
          <label>备注信息：</label>
          <Input.TextArea
            v-model:value="reserveForm.remark"
            placeholder="请输入备注信息（可选）"
            :rows="3"
          />
        </div>
      </div>
    </a-modal>
  </div>
</template>
<script setup>
import {ref, reactive, onMounted} from 'vue'
import {message, Modal, Form, Input, DatePicker, TimePicker} from "ant-design-vue";
import dayjs from 'dayjs'
import Header from '/@/views/index/components/header.vue'
import Footer from '/@/views/index/components/footer.vue'
import {useRouter, useRoute} from 'vue-router'
import {useUserStore} from '/@/store'
import {detailApi, reserveProductApi} from '/@/api/index/product'
import { getImageUrl } from '/@/utils/url'
import { createOrder } from '/@/api/index/order'
import {createApi as createCommentApi, listProductCommentsApi, deleteApi as deleteCommentApi} from '/@/api/index/comment'
import { addProductCollectUserApi, getUserCollectListApi, removeProductCollectUserApi } from '/@/api/index/productCollect'
import AvatarImg from '/@/assets/images/avatar.jpg'
import { CalendarOutlined, HeartOutlined, HeartFilled, DeleteOutlined } from '@ant-design/icons-vue' 

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 商品详情数据
const detailData = ref({
  cover: '',
  title: '',
  price: 0,
  status: 1,
  location: '',
  create_time: '',
  user_name: '',
  views: 0,
  category_name: ''
})

// 评论
const commentList = ref([])
const commentForm = ref({ content: '' })
const isFavorited = ref(false)

// 预约表单
const showReserveModal = ref(false)
const reserveLoading = ref(false)
const reserveForm = ref({
  reserve_time: '',
  reserve_time_time: '',
  trade_location: '',
  remark: ''
})

onMounted(() => {
  const productId = String(route.query.id || '').trim()
  if (productId) {
    getProductDetail(productId)
    loadComments(productId)
    checkFavorite(productId)
  }
})

const getProductDetail = (id) => {
  detailApi({id: id}).then(res => {
    detailData.value = res.data
    // 将backend返回的product_title映射为title
    detailData.value.title = res.data.product_title
    // 将backend返回的product_price_yuan映射为price
    detailData.value.price = res.data.product_price_yuan
    // 将backend返回的location映射为location（如果没有则使用默认值）
    detailData.value.location = res.data.location || '未知地点'
    // 映射商品状态
    detailData.value.status = res.data.product_status
    // 设置商品封面图片
    if (res.data.images && res.data.images.length > 0) {
      detailData.value.cover = getImageUrl(String(res.data.images[0].image_url || ''))
    } else {
      detailData.value.cover = ''
    }
  }).catch(err => {
    message.error('获取商品详情失败')
  })
}

const loadComments = (productId) => {
  listProductCommentsApi({ productId }).then(res => {
    const list = Array.isArray(res.data) ? res.data : []
    commentList.value = list.map(it => ({
      ...it,
      avatar: getImageUrl(it.avatar || it.user_avart || ''),
    }))
  }).catch(() => {})
}

const handleCreateComment = () => {
  const content = commentForm.value.content?.trim()
  if (!userStore.user_id) {
    message.warn('请先登录')
    router.push({name:'login'})
    return
  }
  if (!content) {
    message.warn('评论内容不能为空')
    return
  }
  const productId = String(route.query.id || '').trim()
  createCommentApi({ content, product_id: Number(productId) }).then(() => {
    message.success('评论成功')
    commentForm.value.content = ''
    loadComments(productId)
  }).catch(err => {
    message.error(err.msg || '评论失败')
  })
}

const handleDeleteComment = (c) => {
  deleteCommentApi({ ids: String(c.comment_id) }).then(() => {
    message.success('已删除')
    const productId = String(route.query.id || '').trim()
    loadComments(productId)
  }).catch(err => {
    message.error(err.msg || '删除失败')
  })
}


const checkFavorite = (productId) => {
  getUserCollectListApi({ page: 1, page_size: 100 }).then(res => {
    const list = (res.data && res.data.list) ? res.data.list : []
    isFavorited.value = list.some(i => String(i.product_id) === String(productId))
  }).catch(() => { isFavorited.value = false })
}

const handleToggleFavorite = () => {
  const id = String(route.query.id || '').trim()
  if (!userStore.user_id) {
    message.warn('请先登录')
    router.push({name:'login'})
    return
  }
  if (isFavorited.value) {
    removeProductCollectUserApi({ product_id: id }).then(() => {
      isFavorited.value = false
      message.success('已取消收藏')
    }).catch(err => {
      message.error(err.msg || '取消失败')
    })
  } else {
    addProductCollectUserApi({ product_id: id }).then(() => {
      isFavorited.value = true
      message.success('已加入收藏')
    }).catch(err => {
      message.warn(err.msg || '该商品已在收藏')
      isFavorited.value = true
    })
  }
}

const handleReserve = () => {
  const userId = userStore.user_id
  if (!userId) {
    message.warn('请先登录')
    router.push({name: 'login'})
    return
  }
  if (!reserveForm.value.reserve_time) {
    message.warn('请选择预约时间')
    return
  }
  if (!reserveForm.value.trade_location) {
    message.warn('请输入交易地点')
    return
  }
  const id = String(route.query.id || '').trim()
  if (reserveLoading.value) return

  // 组合日期与时间（Antd 返回 dayjs 对象）并格式化为后端期望的字符串
  let dateStr = ''
  let timeStr = ''
  const d = reserveForm.value.reserve_time
  const t = reserveForm.value.reserve_time_time
  if (d) {
    // dayjs 对象有 format 方法
    dateStr = (typeof d.format === 'function') ? d.format('YYYY-MM-DD') : String(d).trim().slice(0, 10)
  }
  if (t) {
    timeStr = (typeof t.format === 'function') ? t.format('HH:mm') : String(t).trim()
  }
  const reserveTime = timeStr ? `${dateStr} ${timeStr}` : dateStr

  // 使用 dayjs 校验格式及是否早于当前时间
  const selected = timeStr ? dayjs(reserveTime, 'YYYY-MM-DD HH:mm') : dayjs(reserveTime, 'YYYY-MM-DD')
  if (!selected.isValid()) {
    message.warn('预约时间格式不正确')
    return
  }
  if (selected.isBefore(dayjs())) {
    message.warn('预约时间不能早于当前时间')
    return
  }

  reserveLoading.value = true
  reserveProductApi({
    product_id: id,
    reserve_time: reserveTime,
    trade_location: reserveForm.value.trade_location,
    remark: reserveForm.value.remark
  }).then(res => {
    // 预约成功后，后端现在直接创建订单并返回 order_id
    const respData = res?.data || {}
    const orderId = respData.order_id || respData.order_id || null
    if (orderId) {
      message.success('已生成待支付订单')
      showReserveModal.value = false
      router.push({ name: 'pay', query: { id: orderId, amount: detailData.value.price, title: detailData.value.title } })
    } else {
      message.warn('预约成功，但未返回订单信息')
    }
  }).catch(err => {
    reserveLoading.value = false
    message.error(err?.msg || '预约失败')
  }).finally(() => { reserveLoading.value = false })
}
</script>
<style scoped>
.reserve-form {
  padding: 20px 0;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}
</style>
<style scoped lang="less">
.hide {
  display: none;
}

.detail-content {
  display: flex;
  flex-direction: column;
  width: 1100px;
  margin: 4px auto;
}

.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.hidden-lg {
  display: none !important;
}

.product-infos-view {
  display: flex;
  margin: 89px 0 40px;
  overflow: hidden;

  .product-infos {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    display: flex;
  }
}
 .product-img-box {
   width: 420px;
   height: 320px;
   border-radius: 12px;
   overflow: hidden;
   box-shadow: 0 6px 16px rgba(0,0,0,0.06);
 }
 .product-img-box img {
   width: 100%;
   height: 100%;
   object-fit: cover;
   display: block;
 }
 .product-info-box {
   -webkit-box-flex: 1;
   -ms-flex: 1;
   flex: 1;
   padding: 0 24px;
 }
 .product-state {
   display: flex;
   align-items: center;
   gap: 12px;
   color: #6B7280;
 }
 .state {
   padding: 2px 8px;
   border-radius: 999px;
   font-size: 12px;
 }
 .status-on { background: #22c55e; color: #fff; }
 .status-off { background: #9CA3AF; color: #fff; }
 .product-name {
   margin-top: 8px;
   color: #0F1111;
   font-size: 22px;
   font-weight: 600;
 }
 .price {
   margin-top: 16px;
   color: #ef4444;
   font-size: 24px;
   font-weight: 700;
 }
.category-box { margin-top: 16px; }
.action-row { margin-top: 12px; display: flex; gap: 12px; }
.cta-btn {
  transition: transform .08s ease, box-shadow .16s ease, background-color .2s ease, color .2s ease;
}
.cta-btn.ghost {
  background: #fff;
  border: 1px solid #E5E7EB;
}
.cta-btn.favored {
  background: #ef4444;
  color: #fff;
}
.cta-btn:active { transform: scale(0.98); box-shadow: inset 0 2px 8px rgba(0,0,0,0.12); }
.cta-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 18px rgba(0,0,0,0.08); }

.description-card {
  margin-top: 18px;
  background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
  border-radius: 8px;
  padding: 18px;
  box-shadow: 0 6px 20px rgba(16,24,40,0.04);
}
.desc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.desc-title {
  font-size: 16px;
  font-weight: 700;
  color: #0F172A;
}
.desc-meta {
  color: #6B7280;
  font-size: 13px;
  display: flex;
  gap: 12px;
}
.desc-body {
  color: #374151;
  line-height: 1.8;
  white-space: pre-wrap;
}
.count-box { margin-top: 12px; }
.comments .comment-title { font-weight: 600; }
.comments .comment-content { margin-top: 4px; }
</style>
