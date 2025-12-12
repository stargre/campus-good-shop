// 将以下代码复制到浏览器控制台运行，诊断图片加载问题

// 1. 获取商品列表API的响应
fetch('http://localhost:8000/myapp/index/product/list')
  .then(r => r.json())
  .then(data => {
    console.log('=== API返回的原始数据 ===')
    if (data.data && data.data.list && data.data.list[0]) {
      const firstProduct = data.data.list[0]
      console.log('第一个商品:', {
        id: firstProduct.product_id,
        title: firstProduct.product_title,
        cover: firstProduct.cover,
        cover_image_id: firstProduct.cover_image_id
      })
      
      // 2. 测试getImageUrl函数
      console.log('\n=== 测试getImageUrl函数 ===')
      const cover = firstProduct.cover
      console.log('原始cover值:', cover)
      console.log('期望格式: /upload/cover/xxx.jpg')
      
      if (cover) {
        console.log('cover是否以/upload/开头:', cover.startsWith('/upload/'))
        console.log('cover的类型:', typeof cover)
        console.log('cover的长度:', cover.length)
      } else {
        console.log('⚠️ cover为空!')
      }
    } else {
      console.log('❌ 无法获取商品列表或列表为空')
    }
  })
  .catch(e => console.error('API请求失败:', e))
