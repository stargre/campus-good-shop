<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-button type="primary" @click="handleAdd">新增</a-button>
          <a-button @click="handleBatchDelete">批量删除</a-button>
          <a-input-search addon-before="标题" enter-button @search="onSearch" @change="onSearchChange" />
        </a-space>
      </div>
      <a-table
          size="middle"
          rowKey="product_id"
          :loading="data.loading"
          :columns="columns"
          :data-source="data.dataList"
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
              <a @click="handleEdit(record)">编辑</a>
              <a-divider type="vertical" />
              <a-popconfirm title="确定删除?" ok-text="是" cancel-text="否" @confirm="confirmDelete(record)">
                <a href="#">删除</a>
              </a-popconfirm>
            </span>
          </template>
          <template v-else-if="column.key === 'product_status'">
            <span>{{ getStatusText(text) }}</span>
          </template>
          <template v-else-if="column.key === 'quality'">
            <span>{{ getQualityText(text) }}</span>
          </template>
        </template>
      </a-table>
    </div>

    <!--弹窗区域-->
    <div>
      <a-modal
          :visible="modal.visible"
          :forceRender="true"
          :title="modal.title"
          width="880px"
          ok-text="确认"
          cancel-text="取消"
          @cancel="handleCancel"
          @ok="handleOk"
      >
        <div>
          <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form" :rules="modal.rules">
            <a-row :gutter="24">
              <a-col span="24">
                <a-form-item label="商品标题" name="product_title">
                  <a-input placeholder="请输入" v-model:value="modal.form.product_title"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="分类" name="category_id">
                  <a-select placeholder="请选择"
                            allowClear
                            :options="modal.categoryData"
                            :field-names="{ label: 'category_name', value: 'category_id'}"
                            v-model:value="modal.form.category_id">
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="24">
                <a-form-item label="商品描述">
                  <a-textarea placeholder="请输入" v-model:value="modal.form.content"></a-textarea>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="商品原价（元）" name="product_o_price">
                  <a-input-number  placeholder="请输入" :min="0" v-model:value="modal.form.product_o_price" style="width: 100%;"></a-input-number>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="商品现价（元）" name="product_price">
                  <a-input-number  placeholder="请输入" :min="0" v-model:value="modal.form.product_price" style="width: 100%;"></a-input-number>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="商品成色" name="quality">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.quality">
                    <a-select-option key="1" value="1">全新</a-select-option>
                    <a-select-option key="2" value="2">几乎全新</a-select-option>
                    <a-select-option key="3" value="3">轻微使用痕迹</a-select-option>
                    <a-select-option key="4" value="4">明显使用痕迹</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="商品状态" name="product_status">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.product_status">
                    <a-select-option key="0" value="0">待审核</a-select-option>
                    <a-select-option key="1" value="1">审核通过</a-select-option>
                    <a-select-option key="2" value="2">审核不通过</a-select-option>
                    <a-select-option key="3" value="3">已售出</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FormInstance, message, SelectProps } from 'ant-design-vue';
import { createApi, listApi, updateApi, deleteApi } from '/@/api/admin/product';
import {listApi as listCategoryApi} from '/@/api/admin/category'
import {BASE_URL} from "/@/store/constants";
import { onMounted, reactive, ref } from 'vue';

const columns = reactive([
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    width: 60
  },
  {
    title: '标题',
    dataIndex: 'product_title',
    key: 'product_title'
  },
  {
    title: '分类',
    dataIndex: 'category_name',
    key: 'category_name'
  },
  {
    title: '原价',
    dataIndex: 'product_o_price_yuan',
    key: 'product_o_price_yuan',
    customRender: ({ text }) => `¥${text}`
  },
  {
    title: '现价',
    dataIndex: 'product_price_yuan',
    key: 'product_price_yuan',
    customRender: ({ text }) => `¥${text}`
  },
  {
    title: '成色',
    dataIndex: 'quality',
    key: 'quality'
  },
  {
    title: '状态',
    dataIndex: 'product_status',
    key: 'product_status'
  },
  {
    title: '发布时间',
    dataIndex: 'create_time',
    key: 'create_time'
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

// 获取状态文本
const getStatusText = (status: number) => {
  const statusMap = { 0: '待审核', 1: '审核通过', 2: '审核不通过', 3: '已售出' };
  return statusMap[status] || '未知';
};

// 获取成色文本
const getQualityText = (quality: number) => {
  const qualityMap = { 1: '全新', 2: '几乎全新', 3: '轻微使用痕迹', 4: '明显使用痕迹' };
  return qualityMap[quality] || '未知';
};

// 文件列表
const fileList = ref<any[]>([]);

// 处理图片上传
const handleImageUpload = async (file: any) => {
  // 实际项目中应该调用图片上传接口
  // 这里为了演示，直接返回一个模拟的URL
  console.log('Uploading file:', file);
  return false; // 阻止默认上传行为，等待表单提交时统一处理
};

// 页面数据
const data = reactive({
  dataList: [],
  loading: false,
  keyword: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
});

// 弹窗数据源
const modal = reactive({
  visible: false,
  editFlag: false,
  title: '',
  categoryData: [],
  form: {
    product_id: undefined,
    product_title: undefined,
    category_id: undefined,
    categorys: [],
    content: undefined,
    product_o_price: undefined,
    product_price: undefined,
    product_status: undefined,
    quality: undefined,
    reject_reason: undefined
  },
  rules: {
    product_title: [{ required: true, message: '请输入商品标题', trigger: 'change' }],
    category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
    product_o_price: [{ required: true, message: '请输入商品原价', trigger: 'change' }],
    product_price: [{ required: true, message: '请输入商品现价', trigger: 'change' }],
    product_status: [{ required: true, message: '请选择状态', trigger: 'change' }],
    quality: [{ required: true, message: '请选择商品成色', trigger: 'change' }]
  },
});

const myform = ref<FormInstance>();

onMounted(() => {
  getDataList();
  getCategoryDataList();
});

const getDataList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
    page: data.page,
    page_size: data.pageSize
  })
      .then((res) => {
        data.loading = false;
        const list = (res.data && res.data.list) ? res.data.list : []
        list.forEach((item: any, index: any) => {
          item.index = index + 1;
        });
        data.dataList = list;
        if (res.data && typeof res.data.total === 'number') {
          // 如果后端返回分页信息，则同步
          data.page = res.data.page || data.page;
          data.pageSize = res.data.page_size || data.pageSize;
        }
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
        message.error('获取商品列表失败');
      });
}

const getCategoryDataList = () => {
  listCategoryApi({}).then(res => {
    modal.categoryData = res.data
  }).catch(err => {
    console.log(err);
    message.error('获取分类列表失败');
  })
}

const onSearchChange = (e: Event) => {
  data.keyword = e?.target?.value;
  console.log(data.keyword);
};

const onSearch = () => {
  getDataList();
};

const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
});

const handleAdd = () => {
  resetModal();
  modal.visible = true;
  modal.editFlag = false;
  modal.title = '新增商品';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
};
const handleEdit = (record: any) => {
  resetModal();
  modal.visible = true;
  modal.editFlag = true;
  modal.title = '编辑商品';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  // 填充表单数据
  modal.form.product_id = record.product_id;
  modal.form.product_title = record.product_title;
  modal.form.category_id   = record.category_id;
  modal.form.content = record.content;
  modal.form.product_o_price = record.product_o_price_yuan; // 使用元为单位
  modal.form.product_price = record.product_price_yuan;     // 使用元为单位
  modal.form.product_status = record.product_status;
  modal.form.quality = record.quality;
  modal.form.reject_reason = record.reject_reason;
  // 处理分类
  if (record.category_id) {
    modal.form.category = record.category_id;
  }
};

const confirmDelete = (record: any) => {
  console.log('delete', record);
  deleteApi({ id: record.product_id })
      .then((res) => {
        message.success('删除成功');
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '操作失败');
      });
};

const handleBatchDelete = () => {
  console.log(data.selectedRowKeys);
  if (data.selectedRowKeys.length <= 0) {
    message.warn('请勾选删除项');
    return;
  }
  // 批量删除暂时实现为多次单条删除，实际项目中应使用批量删除API
  let deleteCount = 0;
  data.selectedRowKeys.forEach(productId => {
    deleteApi({ id: productId })
      .then(() => {
        deleteCount++;
        if (deleteCount === data.selectedRowKeys.length) {
          message.success('批量删除成功');
          data.selectedRowKeys = [];
          getDataList();
        }
      })
      .catch((err) => {
        message.error(err.msg || '操作失败');
      });
  });
};

const handleOk = () => {
  myform.value
      ?.validate()
      .then(() => {
        const formData = {
          ...modal.form
        };
        if (formData.category_id === undefined || formData.category_id === null || formData.category_id === '') {
          delete (formData as any).category_id
        } else {
          (formData as any).category_id = Number(formData.category_id)
        }
        
        // 价格单位保持为元（整数），无需转换
        
        if (modal.editFlag) {
          updateApi({ product_id: formData.product_id || formData.id }, formData)
              .then((res) => {
                message.success('更新成功');
                hideModal();
                getDataList();
              })
              .catch((err) => {
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        } else {
          createApi(formData)
              .then((res) => {
                message.success('创建成功');
                hideModal();
                getDataList();
              })
              .catch((err) => {
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        }
      })
      .catch((err) => {
        console.log('表单验证失败');
      });
};

const handleCancel = () => {
  hideModal();
};

// 恢复表单初始状态
const resetModal = () => {
  myform.value?.resetFields();
  fileList.value = [];
};

// 关闭弹窗
const hideModal = () => {
  modal.visible = false;
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
