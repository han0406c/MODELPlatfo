<template>
  <div class="header-container">
    <div class="header-content">
      <!-- Logo 图片 -->
      <img class="logo" src="../assets/image/logo.png" alt="Logo">
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeaderLine',
}
</script>

<style scoped>
/* 顶部导航栏容器 */
  .header-container {
  background: linear-gradient(25deg, #d6235d ,#ea7a79 , #f8bb97, #fff9b6); /* 渐变背景色 */
  padding: 10px 20px;
  display: flex;
  justify-content: flex-start; /* Logo 左对齐 */
  align-items: center;
  height: 80px; /* 固定高度 */
  border-radius: 12px; /* 圆角处理 */
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15); /* 增强阴影以增加层次感 */
  position: relative;
  z-index: 100; /* 保证在其他元素上方 */
  margin: 10px 10px 10px 0; /* 让 header 的左侧紧贴页面，其他边缘保留间距 */
}

/* Logo 样式 */
.logo {
  width: 100px; /* 设置 Logo 大小 */
  height: auto;
  margin-left: 10px; /* 调整左侧空白 */
  filter: drop-shadow(2px 4px 6px rgba(0, 0, 0, 0.2)); /* 增加logo阴影效果 */
  border-radius: 50%; /* 使 Logo 也具有圆角效果 */
  background-color: #fff; /* 增加背景色与渐变对比 */
  padding: 8px; /* 内边距增加美观 */
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-container {
    height: 70px; /* 在小屏幕时缩小 header 高度 */
  }

  .logo {
    width: 90px; /* 调整小屏幕下的 Logo 大小 */
  }
}
</style>