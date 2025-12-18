<template>
  <div class="content-list">
    <div class="list-title">我的收藏</div>
    <div role="tablist" class="list-tabs-view flex-view">
    </div>
    <div class="list-content">
      <div class="collect-product-view">
        <a-spin :spinning="loading" style="min-height: 200px;">
          <div class="product-list">
          <div class="product-item" v-for="(item,index) in pageData.collectData" :key="index" @click="handleClickItem(item)">
            <button class="remove" @click.stop="handleRemove(item)">移出</button>
            <div class="img-view">
              <img :src="item.cover">
            </div>
            <div class="info-view">
              <h3 class="product-name">{{item.title}}</h3>
              <p class="authors" v-if="item.author">{{item.author}}（作者)</p>
              <p class="translators" v-if="item.translator">{{item.translator}}（译者）</p>
            </div>
          </div>
          <template v-if="!pageData.collectData || pageData.collectData.length <= 0">
            <div class="empty-center">
              <a-empty description="暂无收藏" />
            </div>
          </template>
        </div>
        </a-spin>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {message} from 'ant-design-vue';
import { getUserCollectListApi, removeProductCollectUserApi } from '/@/api/index/productCollect'
import { getImageUrl } from '/@/utils/url'
import {useUserStore} from "/@/store";

const router = useRouter();
const userStore = useUserStore();

const pageData = reactive({
  collectData: []
})

const loading = ref(false)

onMounted(()=>{
  getCollectProductList()
})

const handleClickItem =(record) =>{
  let text = router.resolve({name: 'detail', query: {id: record.product_id}})
  window.open(text.href, '_blank')
}
const handleRemove =(record)=> {
  removeProductCollectUserApi({ product_id: record.product_id }).then(res => {
    message.success('移除成功')
    getCollectProductList()
  }).catch(err => {
    console.log(err)
  })
}
const getCollectProductList =()=> {
  loading.value = true
  getUserCollectListApi({ page: 1, page_size: 100 }).then(res => {
    const list = (res.data && res.data.list) ? res.data.list : []
    list.forEach(item => {
      if (item.product_image) {
        item.cover = getImageUrl(item.product_image)
      }
      item.title = item.product_title
    })
    pageData.collectData = list
    loading.value = false
  }).catch(err => {
    console.log(err.msg)
    loading.value = false
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

  .list-tabs-view {
    position: relative;
    border-bottom: 1px solid #cedce4;
    height: 12px;
    line-height: 42px;
  }
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}
.product-item {
  position: relative;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.06);
  overflow: hidden;
  cursor: pointer;
  transition: transform .12s ease, box-shadow .2s ease;
}
.product-item:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(0,0,0,0.08); }
.product-item:active { transform: scale(0.98); box-shadow: inset 0 2px 8px rgba(0,0,0,0.12); }
.remove {
  position: absolute;
  right: 8px;
  top: 8px;
  padding: 0 10px;
  height: 26px;
  text-align: center;
  line-height: 26px;
  color: #374151;
  background: #ffffff;
  border: 1px solid #E5E7EB;
  border-radius: 999px;
  cursor: pointer;
  transition: transform .08s ease, box-shadow .16s ease, background-color .2s ease;
}
.remove:hover { transform: translateY(-1px); box-shadow: 0 8px 18px rgba(0,0,0,0.08); background: #f9fafb; }
.remove:active { transform: scale(0.98); box-shadow: inset 0 2px 8px rgba(0,0,0,0.12); }
.img-view { height: 180px; width: 100%; overflow: hidden; }
.img-view img { width: 100%; height: 100%; object-fit: cover; display: block; }
.info-view { padding: 12px 16px 16px; text-align: center; }
.info-view h3 { color: #0F1111; font-weight: 500; font-size: 16px; line-height: 20px; margin: 8px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.info-view .authors, .info-view .translators { color: #6B7280; font-size: 12px; line-height: 16px; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
