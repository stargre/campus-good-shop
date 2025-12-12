<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="openCreateModal">新增评论</a-button>
          <a-button @click="handleBatchDelete">批量删除</a-button>
        </a-space>
      </div>
      <a-table
          size="middle"
          rowKey="id"
          :loading="data.loading"
          :columns="columns"
          :data-source="data.list"
          :scroll="{ x: 'max-content' }"
          :row-selection="rowSelection"
          :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          onChange: (current) => (data.page = current),
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
      >
        <template #bodyCell="{ text, record, index, column }">
          <template v-if="column.key === 'operation'">
            <span>
              <a-divider type="vertical"/>
              <a-popconfirm title="确定删除?" ok-text="是" cancel-text="否" @confirm="confirmDelete(record)">
                <a href="#">删除</a>
              </a-popconfirm>
            </span>
          </template>
        </template>
      </a-table>
  </div>

  <!-- 新增评论弹窗 -->
  <a-modal :visible="createModal.visible" title="新增评论" @ok="handleCreate" @cancel="createModal.visible=false">
    <a-form :model="createModal.form" :label-col="{ style: { width: '100px' } }">
      <a-form-item label="商品ID">
        <a-input v-model:value="createModal.form.product_id" placeholder="请输入商品ID" />
      </a-form-item>
      <a-form-item label="用户ID">
        <a-input v-model:value="createModal.form.user_id" placeholder="请输入用户ID" />
      </a-form-item>
      <a-form-item label="评论内容">
        <a-input v-model:value="createModal.form.comment_content" placeholder="请输入评论内容" />
      </a-form-item>
      <a-form-item label="评分(1-10)">
        <a-input v-model:value="createModal.form.rating" placeholder="请输入评分" />
      </a-form-item>
    </a-form>
  </a-modal>
  </div>
</template>

<script setup lang="ts">
import {FormInstance, message} from 'ant-design-vue';
import {createApi, listApi, deleteApi} from '/@/api/admin/comment';
import { listApi as listProductsApi } from '/@/api/admin/product'
import { listApi as listUsersApi } from '/@/api/admin/user'
import {BASE_URL} from "/@/store/constants";
import {getFormatTime} from "/@/utils";

const columns = reactive([
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: '用户',
    dataIndex: 'username',
    key: 'username',
    align: 'center'
  },
  {
    title: '名称',
    dataIndex: 'title',
    key: 'title',
    align: 'center'
  },
  {
    title: '评论内容',
    dataIndex: 'content',
    key: 'content',
    align: 'center'
  },
  {
    title: '评分',
    dataIndex: 'rating',
    key: 'rating',
    align: 'center'
  },
  {
    title: '评论时间',
    dataIndex: 'comment_time',
    key: 'comment_time',
    align: 'center',
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'operation',
    align: 'center',
    fixed: 'right',
    width: 140,
  },
]);

// 页面数据
const data = reactive({
  list: [],
  loading: false,
  currentAdminUserName: '',
  keyword: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
});

// 弹窗数据源
const modal = reactive({
  visile: false,
  editFlag: false,
  title: '',
  form: {
    id: undefined,
    image: undefined,
    link: undefined,
  },
  rules: {
    link: [{required: true, message: '请输入', trigger: 'change'}],
  },
});

onMounted(() => {
  getList();
});

const getList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
  })
      .then((res) => {
        data.loading = false;
        const list = Array.isArray(res.data) ? res.data : []
        data.list = list.map((item: any, index: any) => ({
          id: item.comment_id,
          index: index + 1,
          username: item.buyer_name,
          title: item.product_title,
          content: item.comment_content,
          rating: item.rating,
          comment_time: item.comment_time
        }))
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
      });
};


const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
});

  const createModal = reactive({ visible: false, form: { product_id: '', user_id: '', comment_content: '', rating: 8 } })
  const openCreateModal = () => { createModal.visible = true }
  const handleCreate = async () => {
    const f = createModal.form
    if (!f.product_id || !f.user_id || !f.comment_content) {
      message.warn('请填写必填项')
      return
    }
    try {
      await createApi({ product_id: f.product_id, user_id: f.user_id, comment_content: f.comment_content, rating: f.rating, comment_status: 0 })
      message.success('新增成功')
      createModal.visible = false
      getList()
    } catch (err:any) {
      console.error('新增失败:', err)
      message.error(err?.msg || '新增失败')
    }
  }

const confirmDelete = (record: any) => {
  console.log('delete', record);
  deleteApi({ids: record.id})
      .then((res) => {
        getList();
      })
      .catch((err) => {
        message.error(err.msg || '操作失败');
      });
};

const handleBatchDelete = () => {
  console.log(data.selectedRowKeys);
  if (data.selectedRowKeys.length <= 0) {
    console.log('hello');
    message.warn('请勾选删除项');
    return;
  }
  deleteApi({ids: data.selectedRowKeys.join(',')})
      .then((res) => {
        message.success('删除成功');
        data.selectedRowKeys = [];
        getList();
      })
      .catch((err) => {
        message.error(err.msg || '操作失败');
      });
};
</script>

<style scoped lang="less">
.page-view {
  min-height: 100%;
  background: #fff;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.table-operations {
  margin-bottom: 16px;
  text-align: right;
}

.table-operations > button {
  margin-right: 8px;
}
</style>
