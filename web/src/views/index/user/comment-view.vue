<template>
  <div class="content-list">
    <div class="list-title">我的评论</div>
    <div class="list-content">
      <div class="comment-view">
        <a-spin :spinning="loading" style="min-height: 200px;">
          <div class="comment-list">
            <div class="comment-item flex-view" v-for="item in commentData" :key="item.commentId">
              <img :src="item.avatar || AvatarImg" class="avatar">
              <div class="infos">
                <div class="name flex-view">
                  <h3 @click="handleClickTitle(item)">《{{ item.title || '无标题' }}》</h3>
                  <a-popconfirm
                    v-if="String(item.userId) === String(userStore.user_id)"
                    title="确定删除该评论？"
                    ok-text="是"
                    cancel-text="否"
                    @confirm="handleDelete(item)"
                  >
                    <a-button type="link" danger style="margin-left:12px;">删除</a-button>
                  </a-popconfirm>
                </div>
                <div class="time">{{ getFormatTime(item.commentTime, true) }}</div>
                <div class="content">{{ item.content }}</div>
              </div>
            </div>
            <template v-if="!commentData || commentData.length <= 0">
              <div class="empty-center">
                <a-empty description="暂无评论" />
              </div>
            </template>
          </div>
        </a-spin>
      </div>
    </div>
  </div>
</template>

<script setup>
import AvatarImg from '/@/assets/images/avatar.jpg'
import { getImageUrl } from '/@/utils/url'

import {useUserStore} from "/@/store";

const router = useRouter();
const userStore = useUserStore();

import {listUserCommentsApi} from '/@/api/index/comment'
import {BASE_URL, SERVER_ORIGIN} from "/@/store/constants";
import {getFormatTime} from '/@/utils'

const loading = ref(false)

const commentData = ref([])

onMounted(()=>{
  getCommentList()
})

const handleClickTitle =(record)=> {
  const pid = record.productId || record.product_id || record.productID || record.productid
  if (!pid) return
  let text = router.resolve({name: 'detail', query: {id: pid}})
  window.open(text.href, '_blank')
}

const getCommentList =()=> {
  loading.value = true
  let userId = userStore.user_id
  listUserCommentsApi({userId: userId}).then(res => {
    const list = Array.isArray(res.data) ? res.data : []
    commentData.value = list.map(it => {
      const avatarUrl = getImageUrl(String(it.avatar || it.user_avart || it.user_avatar || ''))
      return {
        commentId: it.comment_id ?? it.id,
        productId: it.product_id ?? it.productId,
        title: it.product_title ?? it.title ?? '',
        content: String(it.comment_content ?? it.content ?? ''),
        commentTime: it.create_time ?? it.create_time ?? '',
        avatar: avatarUrl || '',
        cover: (() => {
          const s = it.cover || ''
          if (!s) return undefined
          if (/^https?:\/\//.test(s)) return s
          if (s.startsWith('/upload/') || s.startsWith('upload/')) return SERVER_ORIGIN + (s.startsWith('/') ? s : ('/' + s))
          return BASE_URL + s
        })(),
        userId: it.user_id ?? it.buyer_id ?? ''
      }
    })
    loading.value = false
  }).catch(err => {
    message.error(err.msg || '网络异常')
    loading.value = false
  })
}

const handleDelete = (item) => {
  if (!item.commentId) return
  deleteApi({ ids: String(item.commentId) }).then(() => {
    message.success('已删除')
    getCommentList()
  }).catch(err => {
    message.error(err.msg || '删除失败')
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
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    //line-height: 24px;
    height: 48px;
    margin-bottom: 4px;
    border-bottom: 1px solid #cedce4;
  }
}

.comment-view {
  overflow: hidden;

  .comment-list {
    margin: 8px auto;
  }

  .comment-item {
    padding: 15px 0;

    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      margin-right: 8px;
    }

    .infos {
      position: relative;
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
    }

    .name {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      cursor: pointer;
    }

    h3 {
      color: #152844;
      font-weight: 600;
      font-size: 14px;
      margin: 0;
    }

    .traingle {
      width: 0;
      height: 0;
      border-left: 6px solid #c3c9d5;
      border-right: 0;
      border-top: 4px solid transparent;
      border-bottom: 4px solid transparent;
      margin: 0 12px;
    }

    .time {
      color: #5f77a6;
      font-size: 12px;
      line-height: 16px;
      height: 16px;
      margin: 2px 0 8px;
    }

    .content {
      color: #484848;
      font-size: 14px;
      line-height: 22px;
      padding-right: 30px;
    }
  }
}
</style>
