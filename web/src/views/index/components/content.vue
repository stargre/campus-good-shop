<template>
  <div class="content">
    <div class="content-left">
      <div class="left-search-item">
        <h4>商品分类</h4>
        <a-tree :tree-data="contentData.cData" :selected-keys="contentData.selectedKeys" @select="onSelect"
                style="min-height: 220px;">
        </a-tree>
      </div>
    </div>
  <div class="content-right">
    <div class="top-select-view flex-view">
      <div class="order-view">
        <span class="title"></span>
        <span class="tab"
              :class="contentData.selectTabIndex===index? 'tab-select':''"
              v-for="(item,index) in contentData.tabData"
              :key="index"
              @click="selectTab(index)">
          {{ item }}
        </span>
        <span :style="{left: contentData.tabUnderLeft + 'px'}" class="tab-underline"></span>
      </div>
      <div class="sold-toggle">
        <a-radio-group v-model:value="contentData.soldFilter" @change="onSoldFilterChange" size="small">
          <a-radio-button value="unsold">未售出</a-radio-button>
          <a-radio-button value="sold">已售出</a-radio-button>
        </a-radio-group>
      </div>
    </div>
      <a-spin :spinning="contentData.loading" style="min-height: 200px;">
        <div class="pc-product-list">
          <div v-for="item in contentData.pageData" :key="item.id" class="product-item" @click="handleDetail(item)">
            <div class="img-view">
              <img :src="item.cover" :alt="item.title" />
            </div>
            <div class="info-view">
              <div class="product-name">{{ item.title }}</div>
              <div class="price">¥{{ item.price }}</div>
              <div class="translators">{{ item.location }}</div>
            </div>
          </div>
          <div v-if="contentData.pageData.length === 0" class="no-data">暂无商品数据</div>
        </div>
      </a-spin>
      <div class="page-view" style="">
        <a-pagination v-model="contentData.page" size="small" @change="changePage" :hideOnSinglePage="true"
                      :defaultPageSize="contentData.pageSize" :total="contentData.total" :showSizeChanger="false"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {listApi as listCategoryList} from '/@/api/index/category'
import {listApi as listProductList} from '/@/api/index/product'
import { getImageUrl } from '/@/utils/url'
import {useUserStore} from "/@/store";
import {message} from "ant-design-vue";

const userStore = useUserStore()
const router = useRouter();

const contentData = reactive({
  selectX: 0,
  cData: [],
  selectedKeys: [],
  loading: false,

  tabData: ['最新', '最热', '推荐'],
  selectTabIndex: 0,
  tabUnderLeft: 12,

  soldFilter: 'unsold',

  productData: [],
  pageData: [],

  page: 1,
  total: 0,
  pageSize: 12,
  lastFilters: {},
})

onMounted(() => {
  initSider()
  // 默认按“最新”排序
  getProductList({ sort: 'recent' }, 1)
})

const initSider = () => {
  contentData.cData.push({key: -1, title:'全部'})
  listCategoryList().then(res => {
    res.data.forEach(item=>{
      item.key = item.id
      contentData.cData.push(item)
    })
  })
}

const getSelectedKey = () => {
  if (contentData.selectedKeys.length > 0) {
    const k = contentData.selectedKeys[0]
    const num = Number(k)
    return isNaN(num) ? -1 : num
  } else {
    return -1
  }
}

const onSelect = (selectedKeys) => {
  contentData.selectedKeys = selectedKeys
  const key = getSelectedKey()
  if (contentData.selectedKeys.length > 0 && key !== -1) {
    getProductList({category_id: key})
  } else {
    getProductList({})
  }
}

// 最新|最热|推荐
const selectTab = (index) => {
  contentData.selectTabIndex = index
  contentData.tabUnderLeft = 12 + 50 * index
  console.log(contentData.selectTabIndex)
  let sort = (index === 0 ? 'recent' : index === 1 ? 'hot' : 'recommend')
  const data = {sort: sort}
  const key = getSelectedKey()
  if (contentData.selectedKeys.length > 0 && key !== -1) {
    data['category_id'] = key
  }
  getProductList(data, 1)
}

const onSoldFilterChange = () => {
  const data = {}
  const key = getSelectedKey()
  if (contentData.selectedKeys.length > 0 && key !== -1) {
    data['category_id'] = key
  }
  getProductList(data, 1)
}

const handleDetail = (item) => {
  // 跳转新页面
  let text = router.resolve({name: 'detail', query: {id: item.id}})
  window.open(text.href, '_blank')
}

// 分页事件
const changePage = (page) => {
  getProductList(contentData.lastFilters || {}, page)
  console.log('第' + page + '页')
}

const getProductList = (data, page = 1) => {
  contentData.loading = true
  const params = { ...data }
  // 默认仅显示未售出：product_status==1；切换“已售出”时传 3
  params['status'] = contentData.soldFilter === 'sold' ? 3 : 1
  params['page'] = page
  params['size'] = contentData.pageSize

  // 记录当前过滤条件（不含分页参数）
  const { page: _p, size: _s, ...filters } = params
  contentData.lastFilters = { ...filters }

  listProductList(params).then(res => {
    contentData.loading = false
    // 适配后端返回的数据结构：res.data包含list和pagination
    const productList = res.data.list || [];
    const pagination = res.data.pagination || {};
    
    productList.forEach((item) => {
      // 兼容不同字段：cover > cover_image
      const rawCover = item.cover || item.cover_image || ''
      if (!rawCover) {
        console.warn('商品缺少cover字段:', item.id || item.product_id, item)
      }
      item.cover = getImageUrl(rawCover)
      console.log('处理后的cover:', item.id || item.product_id, item.cover)
    })
    console.log('处理后的商品列表:', productList)
    contentData.productData = productList
    contentData.pageData = productList
    contentData.total = pagination.total || productList.length
    contentData.page = page
  }).catch(err => {
    console.log(err)
    contentData.loading = false
    message.error("获取商品列表失败")
  })
}

</script>

<style scoped lang="less">
.content {
  display: flex;
  flex-direction: row;
  width: 1100px;
  margin: 80px auto;
}

.content-left {
  width: 220px;
  margin-right: 32px;
}

.left-search-item {
  overflow: hidden;
  border-bottom: 1px solid #cedce4;
  margin-top: 24px;
  padding-bottom: 24px;
}

h4 {
  color: #4d4d4d;
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  height: 24px;
}

.category-item {
  cursor: pointer;
  color: #333;
  margin: 12px 0 0;
  padding-left: 16px;
}

ul {
  margin: 0;
  padding: 0;
}

ul {
  list-style-type: none;
}

li {
  margin: 4px 0 0;
  display: list-item;
  text-align: -webkit-match-parent;
}

.child {
  color: #333;
  padding-left: 16px;
}

.child:hover {
  color: #4684e2;
}

.select {
  color: #4684e2;
}

.flex-view {
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  //justify-content: space-between;
  display: flex;
}

.name {
  font-size: 14px;
}

.name:hover {
  color: #4684e2;
}

.count {
  font-size: 14px;
  color: #999;
}

.check-item {
  font-size: 0;
  height: 18px;
  line-height: 12px;
  margin: 12px 0 0;
  color: #333;
  cursor: pointer;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}

.check-item input {
  cursor: pointer;
}

.check-item label {
  font-size: 14px;
  margin-left: 12px;
  cursor: pointer;
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
}

.category-view {
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  margin-top: 4px;
}

.category-flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.category {
  background: #fff;
  border: 1px solid #a1adc6;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  border-radius: 16px;
  height: 20px;
  line-height: 18px;
  padding: 0 8px;
  margin: 8px 8px 0 0;
  cursor: pointer;
  font-size: 12px;
  color: #152833;
}

.category:hover {
  background: #4684e3;
  color: #fff;
  border: 1px solid #4684e3;
}

.category-select {
  background: #4684e3;
  color: #fff;
  border: 1px solid #4684e3;
}

.content-right {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
  padding-top: 12px;

  .pc-search-view {
    margin: 0 0 24px;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;

    .search-icon {
      width: 20px;
      height: 20px;
      -webkit-box-flex: 0;
      -ms-flex: 0 0 20px;
      flex: 0 0 20px;
      margin-right: 16px;
    }

    input {
      outline: none;
      border: 0px;
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      border-bottom: 1px solid #cedce4;
      color: #152844;
      font-size: 14px;
      height: 22px;
      line-height: 22px;
      -ms-flex-item-align: end;
      align-self: flex-end;
      padding-bottom: 8px;
    }

    .clear-search-icon {
      position: relative;
      left: -20px;
      cursor: pointer;
    }

    button {
      outline: none;
      border: none;
      font-size: 14px;
      color: #fff;
      background: #288dda;
      border-radius: 32px;
      width: 88px;
      height: 32px;
      line-height: 32px;
      margin-left: 2px;
      cursor: pointer;
    }

    .float-count {
      color: #999;
      margin-left: 24px;
    }
  }

  .flex-view {
    display: flex;
  }

  .top-select-view {
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    height: 40px;
    line-height: 40px;

    .type-view {
      position: relative;
      font-weight: 400;
      font-size: 18px;
      color: #5f77a6;

      .type-tab {
        margin-right: 32px;
        cursor: pointer;
      }

      .type-tab-select {
        color: #152844;
        font-weight: 600;
        font-size: 20px;
      }

      .tab-underline {
        position: absolute;
        bottom: 0;
        //left: 22px;
        width: 16px;
        height: 4px;
        background: #4684e2;
        -webkit-transition: left .3s;
        transition: left .3s;
      }
    }

    .order-view {
      position: relative;
      color: #6c6c6c;
      font-size: 14px;

      .title {
        margin-right: 8px;
      }

      .tab {
        color: #999;
        margin-right: 20px;
        cursor: pointer;
      }

      .tab-select {
        color: #152844;
      }

      .tab-underline {
        position: absolute;
        bottom: 0;
        left: 84px;
        width: 16px;
        height: 4px;
        background: #4684e2;
        -webkit-transition: left .3s;
        transition: left .3s;
      }
    }

  }

.pc-product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;

  .product-item {
    position: relative;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    overflow: hidden;
    cursor: pointer;
    transition: transform .12s ease, box-shadow .2s ease;
  }
  .product-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.08);
  }

  .img-view {
    height: 180px;
    width: 100%;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
  }

  .info-view {
    padding: 12px 16px 16px;

    .product-name {
      line-height: 20px;
      margin-top: 4px;
      color: #0F1111;
      font-size: 16px;
      font-weight: 500;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .price {
      color: #ef4444;
      font-size: 18px;
      line-height: 22px;
      margin-top: 6px;
      font-weight: 600;
    }

    .translators {
      color: #6B7280;
      font-size: 12px;
      line-height: 16px;
      margin-top: 6px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }

  .no-data {
    grid-column: 1 / -1;
    height: 200px;
    line-height: 200px;
    text-align: center;
    width: 100%;
    font-size: 16px;
    color: #152844;
  }
}

  .page-view {
    width: 100%;
    text-align: center;
    margin-top: 48px;
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
