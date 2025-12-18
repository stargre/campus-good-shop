<template>
  <div class="content-list">
    <div class="list-title">我的订单</div>
  <a-tabs default-active-key="1" @change="onTabChange">
      <a-tab-pane key="1" tab="全部">
      </a-tab-pane>
      <a-tab-pane key="2" tab="待付款">
      </a-tab-pane>
      <a-tab-pane key="3" tab="已支付">
      </a-tab-pane>
      <a-tab-pane key="4" tab="已发货">
      </a-tab-pane>
      <a-tab-pane key="5" tab="已退款">
      </a-tab-pane>
      <a-tab-pane key="6" tab="已完成">
      </a-tab-pane>
      <a-tab-pane key="7" tab="已取消">
      </a-tab-pane>
    </a-tabs>
    <a-spin :spinning="loading" style="min-height: 200px;">
      <div class="list-content">
      <div class="order-item-view" v-for="(item, index) in orderData" :key="index">
        <div class="header flex-view">
          <div class="left">
            <span class="text">订单号</span>
            <span class="num mg-4">#</span>
            <span class="num">{{item.order_id}}</span>
            <span class="time">{{item.create_time}}</span>
          </div>
          <div class="right">
            <a-popconfirm
              v-if="item.order_status===0"
              title="确定取消订单？"
              ok-text="是"
              cancel-text="否"
              @confirm="handleCancel(item)"
            >
              <a-button type="primary" size="small" style="margin-right: 24px;">取消</a-button>
            </a-popconfirm>
            <span class="text">订单状态</span>
            <span class="state">{{item.order_status_text}}</span>
            <a-button v-if="Number(item.order_status)===1 && Number(item.seller_id)===Number(userStore.user_id)" type="primary" size="small" @click="handleDeliver(item)">发货</a-button>
            <a-button v-if="Number(item.order_status)===1 && Number(item.seller_id)===Number(userStore.user_id)" type="default" size="small" style="margin-left:8px" @click="handleRefund(item)">退款</a-button>
          </div>
        </div>
        <div class="content flex-view">
          <div class="left-list">
            <div class="list-item flex-view" v-for="gwcItem in item.gwcData">
              <div class="detail flex-between flex-view">
                <div class="flex-between flex-top flex-view">
                  <h2 class="name">{{gwcItem.title}}</h2>
                  <span class="count">x{{gwcItem.count}}</span>
                </div>
                <div class="flex-between flex-center flex-view">
                  <span class="type"></span>
                  <span class="price">¥{{gwcItem.price}}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="right-info">
            <p class="title">交易信息</p>
            <p class="name">卖家：{{item.seller_name || '未知'}}</p>
            <p class="text mg">买家：{{item.buyer_name || '未知'}}，创建：{{item.create_time}}</p>
            <p class="title">备注信息</p>
            <p class="text">{{item.remark}}</p>
          </div>
        </div>
        <div class="bottom flex-view">
          <div class="left">
            <span class="text">共{{item.gwcData.length}}件商品</span>
          </div>
          <div class="right flex-view">
            <span class="text">总计</span>
            <span class="num">¥ {{item.price}}</span>
            <span class="text">优惠</span>
            <span class="num">¥0</span>
            <span class="text">实际支付</span>
            <span class="money">¥ {{item.price}}</span>
          </div>
        </div>
      </div>
      <template v-if="!orderData || orderData.length <= 0">
        <div class="empty-center">
          <a-empty description="暂无订单" />
        </div>
      </template>
    </div>
    </a-spin>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useRouter, useRoute } from 'vue-router'
import { getOrderList as getOrderListApi, cancelOrder, deliverOrder, refundOrder } from '/@/api/index/order'
import { BASE_URL } from '/@/store/constants'
import { useUserStore } from '/@/store'

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const loading = ref(false)
const orderData = ref([])
const orderStatus = ref('')

onMounted(()=>{
  getOrderList()
})

const onTabChange =(key)=> {
  console.log(key)
  if (key === '1') {
    orderStatus.value = ''
  }
  if (key === '2') {
    orderStatus.value = '0'
  }
  if (key === '3') {
    orderStatus.value = '1'
  }
  if (key === '4') {
    orderStatus.value = '2'
  }
  if (key === '5') {
    orderStatus.value = '5'
  }
  if (key === '6') {
    orderStatus.value = '3'
  }
  if (key === '7') {
    orderStatus.value = '4'
  }
  getOrderList()
}
const getOrderList= ()=> {
  loading.value = true
  getOrderListApi({orderStatus: orderStatus.value}).then(res => {
    const list = Array.isArray(res.data) ? res.data : []
    // 适配后端订单结构到前端展示结构
    orderData.value = list.map((item)=>{
      const gwcData = [{ title: item.product_title, price: item.price, count: 1 }]
      return {
        ...item,
        gwcData
      }
    })
    loading.value = false
  }).catch(err => {
    console.log(err)
    loading.value = false
  })
}
const handleDetail =(productId) =>{
  // 跳转新页面
  let text = router.resolve({name: 'detail', query: {id: productId}})
  window.open(text.href, '_blank')
}
const handleCancel =(item)=> {
  cancelOrder({
    order_id: item.order_id
  }).then(res => {
    message.success('取消成功')
    getOrderList()
  }).catch(err => {
    message.error(err.msg || '取消失败')
  })
}

const handleDeliver = (item) => {
  deliverOrder(item.order_id).then(() => {
    message.success('已发货')
    getOrderList()
  }).catch(err => {
    message.error(err.msg || '发货失败')
  })
}

const handleRefund = (item) => {
  refundOrder(item.order_id).then(() => {
    message.success('退款成功')
    getOrderList()
  }).catch(err => {
    message.error(err.msg || '退款失败')
  })
}

</script>
<style scoped lang="less">
.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.content-list {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    line-height: 24px;
    height: 24px;
    margin-bottom: 4px;
  }
}

.order-item-view {
  background: #f7f9fb;
  border-radius: 4px;
  padding: 16px;
  margin-top: 12px;

  .header {
    border-bottom: 1px solid #cedce4;
    padding-bottom: 12px;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    font-size: 14px;

    .text {
      color: #6f6f6f;
    }

    .mg-4 {
      margin-left: 4px;
    }

    .num {
      font-weight: 500;
      color: #152844;
    }

    .num {
      font-weight: 500;
      color: #152844;
    }

    .time {
      margin-left: 16px;
      color: #a1adc5;
    }

    .state {
      color: #ff7b31;
      font-weight: 600;
      margin-left: 10px;
    }
  }

  .content {
    padding: 12px 0;
    overflow: hidden;

    .left-list {
      overflow: hidden;
      //height: 132px;
      -webkit-box-flex: 2;
      -ms-flex: 2;
      flex: 2;
      padding-right: 16px;

      .list-item {
        height: 60px;
        margin-bottom: 12px;
        overflow: hidden;
        cursor: pointer;
      }

      .product-img {
        width: 48px;
        height: 100%;
        margin-right: 12px;
      }

      .detail {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
      }

      .flex-between {
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
        justify-content: space-between;
      }

      .flex-between {
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
        justify-content: space-between;
      }

      .flex-top {
        -webkit-box-align: start;
        -ms-flex-align: start;
        align-items: flex-start;
      }

      .name {
        color: #152844;
        font-weight: 600;
        font-size: 14px;
        line-height: 18px;
      }

      .count {
        color: #484848;
        font-size: 12px;
      }

      .flex-between {
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
        justify-content: space-between;
      }

      .flex-center {
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
      }

      .type {
        color: #6f6f6f;
        font-size: 12px;
      }

      .price {
        color: #ff7b31;
        font-weight: 600;
        font-size: 14px;
      }
    }

    .right-info {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      border-left: 1px solid #cedce4;
      padding-left: 12px;
      line-height: 22px;
      font-size: 14px;

      .title {
        color: #6f6f6f;
      }

      .name {
        color: #152844;
      }

      .text {
        color: #484848;
      }

      .mg {
        margin-bottom: 4px;
      }
    }
  }

  .bottom {
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    border-top: 1px solid #cedce4;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    font-size: 14px;
    padding-top: 14px;

    .text {
      color: #6f6f6f;
    }

    .open {
      color: #4684e2;
      margin-left: 8px;
      cursor: pointer;
    }

    .right {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
    }

    .text {
      color: #6f6f6f;
    }

    .num {
      color: #152844;
      margin: 0 40px 0 8px;
    }

    .money {
      font-weight: 600;
      font-size: 18px;
      color: #ff7b31;
      margin-left: 8px;
    }
  }

}

.order-item-view:first-child {
  margin-top: 16px;
}

</style>
const handleDeliver = (item) => {
  deliverOrder(item.order_id).then(()=>{
    message.success('已发货')
    getOrderList()
  }).catch(err=>{
    message.error(err.msg||'发货失败')
  })
}
