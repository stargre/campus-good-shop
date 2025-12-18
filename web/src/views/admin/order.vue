<template>
  <div class="page-view">
    <!-- 搜索和操作区域 -->
    <div class="table-operations">
      <a-input-search
        placeholder="搜索商品标题、买家或卖家"
        allowClear
        enterButton="搜索"
        style="width: 300px; margin-right: 16px;"
        @search="onSearch"
        @change="onSearchChange"
      />
      <a-select
        v-model:value="data.order_status"
        placeholder="订单状态"
        style="width: 120px; margin-right: 16px;"
        @change="getDataList"
      >
        <a-select-option value="">全部</a-select-option>
        <a-select-option value="0">待支付</a-select-option>
        <a-select-option value="1">已支付</a-select-option>
        <a-select-option value="2">已发货</a-select-option>
        <a-select-option value="3">已完成</a-select-option>
        <a-select-option value="4">已取消</a-select-option>
        <a-select-option value="5">退款中</a-select-option>
      </a-select>
      <a-button type="primary" @click="handleBatchDelete" :disabled="data.selectedRowKeys.length === 0">批量删除</a-button>
    </div>

    <!-- 订单列表 -->
    <a-table
      :columns="columns"
      :data-source="data.orderList"
      :pagination="{
        current: data.page,
        pageSize: data.pageSize,
        total: data.total,
        onChange: (page, pageSize) => {
          data.page = page;
          data.pageSize = pageSize;
          getDataList();
        },
      }"
      :loading="data.loading"
      :row-selection="rowSelection"
      row-key="order_id"
    >
      <template #bodyCell="{ column, record }">
        <!-- 订单状态 -->
        <template v-if="column.key === 'order_status'">
          <a-tag
            :color="getOrderStatusColor(record.order_status)"
          >
            {{ record.order_status_text }}
          </a-tag>
        </template>
        <!-- 价格 -->
        <template v-else-if="column.key === 'price'">
          ¥{{ record.price }}
        </template>
        <!-- 操作列 -->
        <template v-else-if="column.key === 'operation'">
          <a-button type="text" size="small" @click="handleUpdateStatus(record)">更新状态</a-button>
          <a-button type="text" size="small" danger @click="confirmDelete(record)">删除</a-button>
        </template>
      </template>
    </a-table>

    <!-- 更新状态弹窗 -->
    <a-modal
      v-model:visible="modal.visile"
      :title="modal.title"
      :width="400"
      ok-text="确认"
      cancel-text="取消"
      @ok="handleOk"
      @cancel="handleCancel"
    >
      <div>
        <div class="item">
          <label>订单状态</label>
          <a-select v-model:value="modal.form.order_status">
            <a-select-option value="0">待支付</a-select-option>
            <a-select-option value="1">已支付</a-select-option>
            <a-select-option value="2">已发货</a-select-option>
            <a-select-option value="3">已完成</a-select-option>
            <a-select-option value="4">已取消</a-select-option>
            <a-select-option value="5">已退款</a-select-option>
          </a-select>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { FormInstance, message, Modal as a_modal } from 'ant-design-vue';
import { createApi, listApi, updateApi, deleteApi } from '/@/api/admin/order';
import { reactive, ref, onMounted } from 'vue';

// 订单列表列配置
const columns = reactive([
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    align: 'center',
    width: 60
  },
  {
    title: '订单号',
    dataIndex: 'order_id',
    key: 'order_id',
    align: 'center',
    width: 120
  },
  {
    title: '商品',
    dataIndex: 'product_title',
    key: 'product_title',
  },
  {
    title: '卖家',
    dataIndex: 'seller_name',
    key: 'seller_name',
    align: 'center',
    width: 120
  },
  {
    title: '买家',
    dataIndex: 'buyer_name',
    key: 'buyer_name',
    align: 'center',
    width: 120
  },
  {
    title: '价格',
    dataIndex: 'price',
    key: 'price',
    align: 'center',
    width: 100
  },
  {
    title: '状态',
    dataIndex: 'order_status',
    key: 'order_status',
    align: 'center',
    width: 120
  },
  {
    title: '创建时间',
    dataIndex: 'create_time',
    key: 'create_time',
    align: 'center',
    width: 160
  },
  {
    title: '支付时间',
    dataIndex: 'pay_time',
    key: 'pay_time',
    align: 'center',
    width: 160
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
  orderList: [],
  loading: false,
  keyword: '',
  order_status: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
  total: 0,
});

// 弹窗数据
const modal = reactive({
  visile: false,
  title: '更新订单状态',
  editFlag: false,
  form: {
    order_id: '',
    order_status: 0,
  },
  rules: {
    order_status: [{ required: true, message: '请选择订单状态', trigger: 'change' }],
  },
});

// 表单引用
const myform = ref<FormInstance>();

// 生命周期
onMounted(() => {
  getDataList();
});

// 获取订单列表
const getDataList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
    order_status: data.order_status,
    page: data.page,
    page_size: data.pageSize
  })
    .then((res) => {
      data.loading = false;
      if (res.code === 0) {
        res.data.list.forEach((item: any, index: any) => {
          item.index = index + 1;
        });
        data.orderList = res.data.list;
        data.total = res.data.total;
        data.page = res.data.page;
        data.pageSize = res.data.page_size;
      } else {
        message.error(res.msg || '获取订单列表失败');
      }
    })
    .catch((err) => {
      data.loading = false;
      console.log(err);
      message.error('获取订单列表失败');
    });
};

// 搜索
const onSearch = (value: string) => {
  data.keyword = value;
  data.page = 1;
  getDataList();
};

const onSearchChange = (e: any) => {
  data.keyword = e.target.value;
};

// 行选择
const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: any[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
});

// 获取订单状态颜色
const getOrderStatusColor = (status: number) => {
  const colorMap: Record<number, string> = {
    0: 'blue',
    1: 'orange',
    2: 'green',
    3: 'cyan',
    4: 'default',
    5: 'red'
  };
  return colorMap[status] || 'default';
};

// 更新订单状态
const handleUpdateStatus = (record: any) => {
  modal.visile = true;
  modal.editFlag = true;
  modal.title = '更新订单状态';
  modal.form.order_id = record.order_id;
  modal.form.order_status = record.order_status;
};

// 确认删除
const confirmDelete = (record: any) => {
  a_modal.confirm({
    title: '确认删除',
    content: '确定要删除该订单吗？',
    onOk() {
      deleteApi({ order_id: record.order_id })
        .then((res) => {
          if (res.code === 0) {
            message.success('删除成功');
            getDataList();
          } else {
            message.error(res.msg || '删除失败');
          }
        })
        .catch((err) => {
          console.log(err);
          message.error('删除失败');
        });
    }
  });
};

// 批量删除
const handleBatchDelete = () => {
  a_modal.confirm({
    title: '确认批量删除',
    content: `确定要删除选中的${data.selectedRowKeys.length}个订单吗？`,
    onOk() {
      deleteApi({ ids: data.selectedRowKeys.join(',') })
        .then((res) => {
          if (res.code === 0) {
            message.success('批量删除成功');
            data.selectedRowKeys = [];
            getDataList();
          } else {
            message.error(res.msg || '批量删除失败');
          }
        })
        .catch((err) => {
          console.log(err);
          message.error('批量删除失败');
        });
    }
  });
};

// 确认更新
const handleOk = () => {
  const formData = { ...modal.form };
  updateApi({ order_id: formData.order_id }, formData)
    .then((res) => {
      if (res.code === 0) {
        message.success('更新成功');
        hideModal();
        getDataList();
      } else {
        message.error(res.msg || '更新失败');
      }
    })
    .catch((err) => {
      console.log(err);
      message.error('更新失败');
    });
};

// 取消操作
const handleCancel = () => {
  hideModal();
};

// 关闭弹窗
const hideModal = () => {
  modal.visile = false;
  resetModal();
};

// 重置表单
const resetModal = () => {
  myform.value?.resetFields();
  modal.form = {
    order_id: '',
    order_status: 0,
  };
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
    text-align: left;
  }

  .table-operations > button {
    margin-right: 8px;
  }
</style>
