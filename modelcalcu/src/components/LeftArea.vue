<template>
  <div class="leftbg">
    <!-- 模型库 -->
    <div class="leftitem" :class="{ highlighting: chooseModule == 1 }" @click="changeModule(1)">
      模型库
    </div>
    <!-- 模型实例 -->
    <div class="leftitem" :class="{ highlighting: chooseModule == 2 }" @click="changeModule(2)">
      模型实例
    </div>
  </div>
</template>

<script>
export default {
  name: "LeftArea",
  props: {
    chooseModule: Number,
    changeModule: Function,
  },
}
</script>

<style scoped>
/* 确保 body 和 html 高度为 100% */
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

/* 背景区域 */
.leftbg {
  width: 15%; /* 使用百分比宽度，背景区域占据页面的 15% 宽度 */
  min-width: 150px; /* 设置最小宽度，避免太小 */
  height: 100vh; /* 使用视口高度确保左边栏占满整个高度 */
  background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%); /* 渐变背景 */
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center; /* 背景区域内居中对齐 */
  padding: 10px 0;
  border-radius: 12px; /* 设置整个背景的圆角 */
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* 轻微阴影 */
}

/* 左侧菜单项 */
.leftitem {
  width: 101%; /* 相对背景区域设置按钮宽度为 90% */
  margin: 15px 0; /* 上下边距 */
  padding: 25px 0; /* 内边距，控制按钮高度 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  font-size: 22px; /* 调整字体大小 */
  font-weight: 600;
  color: #333;
  background-color: rgba(255, 255, 255, 0.8); /* 增加透明白色背景 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* 增加轻微的阴影效果 */
  transition: all 0.3s ease; /* 增加过渡动画 */
  cursor: pointer;
  border-radius: 12px; /* 按钮圆角 */
}

/* 选中高亮的效果 */
.highlighting {
  background-color: #4facfe;
  color: white;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* 增加阴影 */
  transform: scale(1.05); /* 点击后放大一点点 */
}

/* 鼠标悬停效果 */
.leftitem:hover {
  background-color: rgba(255, 255, 255, 1); /* 鼠标悬停时背景变亮 */
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* 增强阴影效果 */
  transform: scale(1.03); /* 鼠标悬停时略微放大 */
}
</style>