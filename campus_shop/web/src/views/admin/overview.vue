<template>

  <a-spin :spinning="showSpin">
    <div class="main">
      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="商品总数">
            <template #extra>
              <a-tag color="blue">总</a-tag>
            </template>

            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ tdata.data.product_count }}<span class="v-e">种</span></span>
              </div>
              <div class="box-bottom">
                <span>本周新增 {{ tdata.data.product_week_count }} 种</span>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="未付订单">
            <template #extra>
              <a-tag color="green">未付</a-tag>
            </template>
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ tdata.data.order_not_pay_count }}<span class="v-e">单</span></span>
              </div>
              <div class="box-bottom">
                <span>共 {{ tdata.data.order_not_pay_p_count }} 人</span>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="已付订单">
            <template #extra>
              <a-tag color="blue">已付</a-tag>
            </template>
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ tdata.data.order_payed_count }}<span class="v-e">单</span></span>
              </div>
              <div class="box-bottom">
                <span>共 {{ tdata.data.order_payed_p_count }} 人</span>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="取消订单">

            <template #extra>
              <a-tag color="green">取消</a-tag>
            </template>

            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ tdata.data.order_cancel_count }}<span class="v-e">单</span></span>
              </div>
              <div class="box-bottom">
                <span>共 {{ tdata.data.order_cancel_p_count }} 人</span>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>

      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="评论总数">
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ tdata.data.comment_count || 0 }}<span class="v-e">条</span></span>
              </div>
            </div>
          </a-card>
        </a-col>
        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="用户总数">
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ tdata.data.user_count || 0 }}<span class="v-e">人</span></span>
              </div>
            </div>
          </a-card>
        </a-col>
        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="分类总数">
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ tdata.data.category_count || 0 }}<span class="v-e">类</span></span>
              </div>
            </div>
          </a-card>
        </a-col>
        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="订单总数">
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ tdata.data.order_count || 0 }}<span class="v-e">单</span></span>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>

<!--      <a-row :gutter="[20,20]">-->
<!--        <a-col :sm="24" :md="24" :lg="12">-->
<!--          <a-card title="热门菜品排名" style="flex:1;">-->
<!--            <div style="height: 300px;" ref="barChartDiv"></div>-->
<!--          </a-card>-->
<!--        </a-col>-->
<!--        <a-col :sm="24" :md="24" :lg="12">-->
<!--          <a-card title="热门分类比例" style="flex:1;">-->
<!--            <div style="height: 300px;" ref="pieChartDiv"></div>-->
<!--          </a-card>-->
<!--        </a-col>-->
<!--      </a-row>-->

    </div>
  </a-spin>

</template>

<script setup lang="ts">
import {ref, reactive, onMounted} from 'vue';

import { InteractionOutlined, StarFilled, StarTwoTone } from '@ant-design/icons-vue';
import {listApi} from '/@/api/admin/overview'

let showSpin = ref(true)

let tdata = reactive({
  data: {}
})

onMounted(() => {
  list()
})

const list = () => {
  listApi({}).then(res => {
    tdata.data = res.data || {}
    showSpin.value = false
  }).catch(err => {
    showSpin.value = false
  })
}




</script>

<style lang="less" scoped>

.main {
  height: 100%;
  display: flex;
  gap: 20px;
  flex-direction: column;

  .box {
    padding: 12px;
    display: flex;
    flex-direction: column;

    .box-top {
      display: flex;
      flex-direction: row;
      align-items: center;
    }

    .box-value {
      color: #000000;
      font-size: 32px;
      margin-right: 12px;

      .v-e {
        font-size: 14px;
      }
    }

    .box-bottom {
      margin-top: 24px;
      color: #000000d9;
    }
  }
}

</style>
