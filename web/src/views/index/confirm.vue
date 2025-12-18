<template>
  <div>
    <Header/>
    <div style="padding:60px; text-align:center; font-size:18px;">购物车功能已移除</div>
    <div style="text-align:center; margin-top:20px;">
      <button @click="handleBack">返回首页</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import Header from '/@/views/index/components/header.vue'

const router = useRouter()
const handleBack = () => router.push({ name: 'home' })
</script>

<style scoped>
/* 购物车页面样式已移除，保留占位样式 */
div { font-family: system-ui; }
</style>
        console.log(err);
        console.log('不能为空');
      });
};

const handleCancel = () => {
  hideModal();
};

// 恢复表单初始状态
const resetModal = () => {
  myform.value?.resetFields();
};

// 关闭弹窗
const hideModal = () => {
  modal.visile = false;
};

const onCountChange = (value) => {
  pageData.amount = pageData.price * value
}

const listAddressData = () => {
  listAddressListApi({}).then(res => {
    const list = Array.isArray(res.data) ? res.data : []
    if (list.length > 0) {
      let current = list[0]
      list.forEach(item => {
        if (item.is_default === 1) {
          current = item
        }
      })
      pageData.receiverName = current.receiver_name
      pageData.receiverPhone = current.receiver_phone
      pageData.receiverAddress = current.receiver_address
    }
  }).catch(err => {
    console.log(err)
  })
}

const handleBack = () => {
  router.back()
  console.log('back...')
}
const handleJiesuan = () => {
  const formData = new FormData()
  let userId = userStore.user_id
  if (!userId) {
    message.warn('请先登录！')
    return
  }
  if (!pageData.receiverName) {
    message.warn('请选择地址！')
    return
  }
  formData.append('user', userId)

  let gwcText = localStorage.getItem("gwc");
  formData.append("gwc", gwcText || '');
  formData.append('amount', pageData.amount || '')
  if (pageData.remark) {
    formData.append('remark', pageData.remark)
  }
  formData.append('receiver_name', pageData.receiverName)
  formData.append('receiver_phone', pageData.receiverPhone)
  formData.append('receiver_address', pageData.receiverAddress)
  console.log(formData)
  createOrder(formData).then(res => {
    message.success('请支付订单')
    router.push({'name': 'pay', query: {'amount': pageData.amount}})
    localStorage.setItem("gwc", "");
  }).catch(err => {
    message.error(err.msg || '失败')
  })

}


</script>

<style scoped lang="less">

.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.cart-page {
  width: 1024px;
  min-height: 50vh;
  margin: 100px auto;
}

.left-flex {
  -webkit-box-flex: 17;
  -ms-flex: 17;
  flex: 17;
  padding-right: 20px;
}

.title {
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  justify-content: space-between;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;

  h3 {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    height: 26px;
    line-height: 26px;
    margin: 0;
  }
}

.cart-list-view {
  margin: 4px 0 40px;

  .list-th {
    height: 42px;
    line-height: 42px;
    border-bottom: 1px solid #cedce4;
    color: #152844;
    font-size: 14px;

    .line-1 {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      margin-right: 20px;
    }

    .line-2, .pc-style .cart-list-view .list-th .line-3, .pc-style .cart-list-view .list-th .line-4 {
      width: 65px;
      margin-right: 20px;
    }

    .line-5 {
      width: 50px;
      margin-right: 40px;
    }

    .line-6 {
      width: 28px;
    }
  }
}

.items {
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  margin-top: 20px;

  .book {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-right: 20px;
    cursor: pointer;

    img {
      width: 48px;
      margin-right: 16px;
      border-radius: 4px;
    }

    h2 {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      font-size: 14px;
      line-height: 22px;
      color: #152844;
    }
  }

  .type {
    width: 65px;
    margin-right: 20px;
    color: #152844;
    font-size: 14px;
  }

  .pay {
    color: #ff8a00;
    font-weight: 600;
    font-size: 16px;
    width: 65px;
    margin-right: 20px;
  }

  .num-box {
    width: 80px;
    margin-right: 43px;
    border-radius: 4px;
    border: 1px solid #cedce4;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    height: 32px;
    padding: 0 4px;
  }

  .delete {
    margin-left: 36px;
    width: 24px;
    cursor: pointer;
  }
}

.mb-24 {
  margin-bottom: 24px;
}

.show-txt {
  color: #ff8a00;
  font-size: 14px;
}

.remark {
  width: 100%;
  background: #f6f9fb;
  border: 0;
  border-radius: 4px;
  padding: 6px 12px;
  //color: #152844;
  margin-top: 16px;
  resize: none;
  height: 56px;
  line-height: 22px;
}

.right-flex {
  -webkit-box-flex: 8;
  -ms-flex: 8;
  flex: 8;
  padding-left: 24px;
  border-left: 1px solid #cedce4;
}

.click-txt {
  color: #4684e2;
  font-size: 14px;
  cursor: pointer;
}

.address-view {
  margin: 12px 0 24px;

  .info {
    color: #909090;
    font-size: 14px;

    .info-blue {
      cursor: pointer;
      color: #4684e2;
    }
  }

  .name {
    color: #152844;
    font-weight: 500;
  }

  .tel {
    color: #152844;
    float: right;
  }

  .address {
    color: #152844;
    margin-top: 4px;
  }
}

.price-view {
  overflow: hidden;
  margin-top: 16px;

  .price-item {
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-bottom: 8px;
    font-size: 14px;

    .item-name {
      color: #152844;
    }

    .price-txt {
      font-weight: 500;
      color: #ff8a00;
    }
  }

  .total-price-view {
    margin-top: 12px;
    border-top: 1px solid #cedce4;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: start;
    -ms-flex-align: start;
    align-items: flex-start;
    padding-top: 10px;
    color: #152844;
    font-weight: 500;

    .price {
      color: #ff8a00;
      font-size: 16px;
      height: 36px;
      line-height: 36px;
    }
  }

  .btns-view {
    margin-top: 24px;
    text-align: right;

    .buy {
      background: #fff;
      color: #4684e2;
    }

    .jiesuan {
      cursor: pointer;
      background: #4684e2;
      color: #fff;
    }

    .btn {
      cursor: pointer;
      width: 96px;
      height: 36px;
      line-height: 33px;
      margin-left: 16px;
      text-align: center;
      border-radius: 32px;
      border: 1px solid #4684e2;
      font-size: 16px;
      outline: none;
    }
  }

}

</style>
