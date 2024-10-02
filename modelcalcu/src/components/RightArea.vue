<template>
  <div class="rightbg">
    <div class="module1" v-show="chooseModule == 1">
      <module1 />
    </div>
    <div class="module2" v-show="chooseModule == 2">
      <module2 />
    </div>
  </div>
</template>

<script>
import module1 from './Module1.vue'
import module2 from './Module2.vue'

export default {
  name: "RightArea",
  props: {
    chooseModule: {
      type: Number,
      required: true,
    },
  },
  components: {
    module1,
    module2,
  },
}
</script>

<style scoped>
/* 整体背景设置 */
.rightbg {
  width: 85%;
  height: 100vh; /* 视口高度，确保右侧区域占满全屏 */
  background: linear-gradient(90deg, #f0f4f8 0%, #e0e0e0 100%);
  padding: 20px;
  border-radius: 12px; /* 圆角 */
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1); /* 背景增加阴影 */
  overflow-y: auto; /* 当内容溢出时启用滚动条 */
  transition: all 0.3s ease;
}

.module1, .module2 {
  border-radius: 12px;
  border: 1px solid #ccc;
  padding: 20px 10px;
  background-color: #ffffff;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.module1:hover, .module2:hover {
  transform: translateY(-5px);
  box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.2);
}
</style>