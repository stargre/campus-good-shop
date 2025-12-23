<template>
  <div>
    <Header/>
    <div class="pay-content">
      <div class="title">订单提交成功</div>
      <div class="text time-margin">
        <span>请在 </span>
        <span class="time">{{ ddlTime }}</span>
        <span> 之前付款，超时订单将自动取消</span>
      </div>
      <div class="text">支付金额</div>
      <div class="price">
        <span class="num">{{ amount }}</span>
        <span>元</span>
      </div>
      <div class="pay-choose-view" style="">
        <div class="pay-choose-box flex-view">
          <div class="choose-box" :class="{'choose-box-active': payMethod === 'wechat'}" @click="selectPayMethod('wechat')">
            <WechatOutlined class="pay-icon" />
            <span>微信支付</span>
          </div>
          <div class="choose-box" :class="{'choose-box-active': payMethod === 'alipay'}" @click="selectPayMethod('alipay')">
            <AlipayCircleOutlined class="pay-icon" />
            <span>支付宝</span>
          </div>
        </div>
        <div class="tips">请选择任意一种支付方式</div>
        <div style="text-align:center">
          <button class="pay-btn pay-btn-active" @click="handlePay()">确认支付</button>
          <button class="back-btn" @click="handleBack()" style="margin-left:12px;">返回原界面</button>
          <button class="cancel-btn" @click="handleCancelPay()" style="margin-left:12px;">取消支付</button>
        </div>
      </div>
      <div class="pay-qr-view" style="display: none;">
        <div class="loading-tip" style="">正在生成安全支付二维码</div>
        <div class="qr-box" style="display: none;">
          <div id="qrCode" class="qr">
          </div>
          <div class="tips">请打开微信扫一扫进行支付</div>
          <button class="pay-finish-btn">支付完成</button>
          <button class="back-pay-btn">选择其他支付方式</button>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import Header from '/@/views/index/components/header.vue'
import {message} from "ant-design-vue";
import { WechatOutlined, AlipayCircleOutlined } from '@ant-design/icons-vue';

const route = useRoute();
const router = useRouter();

let ddlTime = ref()
let amount = ref(0)
let title = ref('')
let payMethod = ref('wechat') // 默认选择微信支付

onMounted(() => {
  amount.value = Number(route.query.amount || 0)
  title.value = String(route.query.title || '')
  ddlTime.value = formatDate(new Date().getTime(), 'YY-MM-DD hh:mm:ss')
})

const handlePay = () => {
  const id = Number(route.query.id || 0)
  if (!id) {
    message.error('订单ID缺失')
    return
  }
  
  // 根据选择的支付方式显示不同的提示
  if (payMethod.value === 'wechat') {
    message.info('选择微信支付')
  } else if (payMethod.value === 'alipay') {
    message.info('选择支付宝支付')
  }
  
  // 不实现真实支付，直接进入下一阶段：调用后端支付接口并跳转订单页
  import('/@/api/index/order').then(mod => {
    mod.payOrder(id).then(() => {
      message.success('已支付，订单状态已更新')
      router.push({ name: 'orderView' })
    }).catch(err => {
      message.error(err.msg || '支付失败')
    })
  })
}

const handleBack = () => {
  // 返回上一页或回到订单页
  router.back()
}

const handleCancelPay = () => {
  const id = Number(route.query.id || 0)
  if (!id) {
    message.error('订单ID缺失')
    return
  }
  import('/@/api/index/order').then(mod => {
    mod.cancelOrder({ order_id: id }).then(() => {
      message.success('订单已取消')
      router.push({ name: 'orderView' })
    }).catch(err => {
      message.error(err.msg || '取消失败')
    })
  })
}

const selectPayMethod = (method) => {
  payMethod.value = method
}
const formatDate = (time, format = 'YY-MM-DD hh:mm:ss') => {
  const date = new Date(time)

  const year = date.getFullYear(),
      month = date.getMonth() + 1,
      day = date.getDate() + 1,
      hour = date.getHours(),
      min = date.getMinutes(),
      sec = date.getSeconds()
  const preArr = Array.apply(null, Array(10)).map(function (elem, index) {
    return '0' + index
  })

  const newTime = format.replace(/YY/g, year)
      .replace(/MM/g, preArr[month] || month)
      .replace(/DD/g, preArr[day] || day)
      .replace(/hh/g, preArr[hour] || hour)
      .replace(/mm/g, preArr[min] || min)
      .replace(/ss/g, preArr[sec] || sec)

  return newTime
}

</script>

<style scoped lang="less">
.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.pay-content {
  position: relative;
  margin: 120px auto 0;
  width: 500px;
  background: #fff;
  overflow: hidden;

  .title {
    color: #152844;
    font-weight: 500;
    font-size: 24px;
    line-height: 22px;
    height: 22px;
    text-align: center;
    margin-bottom: 11px;
  }

  .time-margin {
    margin: 11px 0 24px;
  }

  .text {
    height: 22px;
    line-height: 22px;
    font-size: 14px;
    text-align: center;
    color: #152844;
  }

  .time {
    color: #f62a2a;
  }

  .text {
    height: 22px;
    line-height: 22px;
    font-size: 14px;
    text-align: center;
    color: #152844;
  }

  .price {
    color: #ff8a00;
    font-weight: 500;
    font-size: 16px;
    height: 36px;
    line-height: 36px;
    text-align: center;

    .num {
      font-size: 28px;
    }
  }

  .pay-choose-view {
    margin-top: 24px;

    .choose-box {
      width: 140px;
      height: 126px;
      border: 1px solid #cedce4;
      border-radius: 4px;
      text-align: center;
      cursor: pointer;
    }

    .pay-choose-box {
      -webkit-box-pack: justify;
      -ms-flex-pack: justify;
      justify-content: space-between;
      max-width: 300px;
      margin: 0 auto;

      .pay-icon {
        font-size: 40px;
        margin: 24px auto 16px;
        display: block;
      }
    }

    .tips {
      color: #6f6f6f;
      font-size: 14px;
      line-height: 22px;
      height: 22px;
      text-align: center;
      margin: 16px 0 24px;
    }

    .choose-box-active {
      border: 1px solid #4684e2;
    }

    .tips {
      color: #6f6f6f;
      font-size: 14px;
      line-height: 22px;
      height: 22px;
      text-align: center;
      margin: 16px 0 24px;
    }

    .pay-btn {
      cursor: pointer;
      background: #c3c9d5;
      border-radius: 32px;
      width: 104px;
      height: 32px;
      line-height: 32px;
      border: none;
      outline: none;
      font-size: 14px;
      color: #fff;
      text-align: center;
      display: block;
      margin: 0 auto;
    }

    .pay-btn-active {
      background: #4684e2;
    }
  }
}

</style>
