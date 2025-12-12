<template>
  <div class="content-margin">
    <h1 class="search-name-box">{{ tData.keyword }}</h1>
    <div class="search-tab-nav clearfix">
      <div class="tab-text">
        <span>与</span>
        <span class="strong">{{ tData.keyword }}</span>
        <span>相关的内容</span>
      </div>
    </div>
    <div class="content-list">
      <div class="product-list">

        <a-spin :spinning="tData.loading" style="min-height: 200px;">
          <div class="products flex-view">
            <div class="product-item item-column-4" v-for="item in tData.pageData" :key="item.id" @click="handleDetail(item)">
              <div class="img-view">
                <img :src="item.cover"></div>
              <div class="info-view">
                <h3 class="product-name">{{ item.title.substring(0, 12) }}</h3>
                <span>
                  <span class="a-price-symbol">¥</span>
                  <span class="a-price">{{ item.price }}</span>
                </span>
              </div>
            </div>
          </div>
        </a-spin>
        <div class="page-view" style="">
          <a-pagination v-model:value="tData.page" size="small" @change="changePage" :hideOnSinglePage="true"
                        :defaultPageSize="tData.pageSize" :total="tData.total"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {listApi as listProductList} from '/@/api/index/product'
import { getImageUrl } from '/@/utils/url'
import {useUserStore} from "/@/store";

const userStore = useUserStore()
const router = useRouter();
const route = useRoute();

const tData = reactive({
  loading: false,
  keyword: '',
  productData: [],
  pageData: [],

  page: 1,
  total: 0,
  pageSize: 20,
})

onMounted(() => {
  search()
})

// 监听query参数
watch(() => route.query, (newPath, oldPath) => {
  search()
}, {immediate: false});


const search = () => {
  tData.keyword = route.query.keyword.trim()
  getProductList({'keyword': tData.keyword})
}

// 分页事件
const changePage = (page) => {
  tData.page = page
  let start = (tData.page - 1) * tData.pageSize
  tData.pageData = tData.productData.slice(start, start + tData.pageSize)
  console.log('第' + tData.page + '页')
}
const handleDetail = (item) => {
  // 跳转新页面
  let text = router.resolve({name: 'detail', query: {id: item.id}})
  window.open(text.href, '_blank')
}
const getProductList = (data) => {
  tData.loading = true
  listProductList(data).then(res => {
    // 适配后端返回的数据结构：res.data包含list和pagination
    const productList = res.data.list || [];
    const pagination = res.data.pagination || {};
    
    productList.forEach((item) => {
      if (item.cover) {
        item.cover = getImageUrl(item.cover)
      }
    })
    tData.productData = productList
    tData.total = pagination.total || productList.length
    changePage(1)
    tData.loading = false
  }).catch(err => {
    console.log(err)
    tData.loading = false
  })
}

</script>
<style scoped lang="less">
.content-margin {
  margin: 156px 0 100px;
}

.page-view {
  width: 100%;
  text-align: center;
  margin-top: 48px;
}

.search-name-box {
  background: #f5f9fb;
  height: 100px;
  line-height: 100px;
  font-size: 20px;
  color: #152844;
  text-align: center;
  position: fixed;
  top: 56px;
  left: 0;
  z-index: 1;
  width: calc(100% - 8px);
}

.search-tab-nav {
  position: relative;
  padding: 24px 0 16px;
  text-align: center;

  .tab-text {
    float: left;
    color: #5f77a6;
    font-size: 14px;
  }

  .strong {
    color: #152844;
    font-weight: 600;
    margin: 0 4px;
  }
}

.products {
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
}

.flex-view {
  display: flex;
}

.product-item {
  min-width: 255px;
  max-width: 255px;
  position: relative;
  flex: 1;
  margin-right: 20px;
  height: fit-content;
  overflow: hidden;
  margin-top: 26px;
  margin-bottom: 36px;
  cursor: pointer;

  .img-view {
    //text-align: center;
    height: 200px;
    width: 255px;

    img {
      height: 200px;
      width: 255px;
      margin: 0 auto;
      background-size: cover;
      object-fit: cover;
    }
  }

  .info-view {
    //background: #f6f9fb;
    overflow: hidden;
    padding: 0 16px;

    .product-name {
      line-height: 32px;
      margin-top: 12px;
      color: #0F1111 !important;
      font-size: 18px !important;
      font-weight: 400 !important;
      font-style: normal !important;
      text-transform: none !important;
      text-decoration: none !important;
    }

    .price {
      color: #ff7b31;
      font-size: 20px;
      line-height: 20px;
      margin-top: 4px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .translators {
      color: #6f6f6f;
      font-size: 12px;
      line-height: 14px;
      margin-top: 4px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
}

.a-price-symbol {
  top: -0.5em;
  font-size: 12px;
}

.a-price {
  color: #0F1111;
  font-size: 21px;
}

</style>
