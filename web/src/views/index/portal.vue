<template>
  <div class="portal">
    <Header />
    <Content />
    <Footer />
  </div>
</template>
<script>
import Header from '/@/views/index/components/header.vue'
import Footer from '/@/views/index/components/footer.vue'
import Content from '/@/views/index/components/content.vue'
import {Modal} from "ant-design-vue";

export default {
  components: {
    Footer,
    Header,
    Content
  },
  data () {
    return {
    }
  },
  mounted() {
    Modal.info({
      title: '欢迎来到校内闲置商品发布平台',
      content: '使用过程中遇到问题，可以咨询小组成员：1575100890（QQ）',
      onOk() {},
    });
  }
}
</script>
<style scoped lang="less">

</style>
