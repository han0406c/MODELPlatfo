<template>
  <div class="m1margin">
    <div class="oneItem" v-for="item in modellist" :key="item.id">
      <img class="icon" :src="item.iconaddress" alt="模型图标" />
      <div class="rightup">调用次数：<br />{{ modelReferenceCounts[item.id] || 0 }}</div>
      <p class="boldtext">模型名称：{{ item.id }} - {{ item.name }}</p>
      <p class="commontext">模型描述：{{ item.description }}</p>
      <p class="boldtext">
        发布时间：{{ item.update }}<br />
        模型版本号：{{ item.version }}
      </p>
      <p class="rightbottom">开发者：{{ item.creator }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  name: 'ModuleOne',
  data() {
    return {
      modellist: [],            // 模型列表
      modelReferenceCounts: {},  // 模型引用次数
    };
  },
  mounted() {
    this.loadingmodel();            // 加载模型列表
    this.loadReferenceCounts();      // 加载模型引用次数
  },
  methods: {
    // 加载模型列表
    loadingmodel() {
      axios
        .get('/model/modellist.json')
        .then(res => {
          this.modellist = res.data.data;
        })
        .catch(err => {
          ElMessage({
            showClose: true,
            message: '错误: 模型载入失败。' + err,
            type: 'error',
          });
        });
    },

    // 加载引用次数
    loadReferenceCounts() {
      axios
        .get('http://localhost:5050/model/reference-counts') // 修改路径到引用统计API
        .then(res => {
          if (typeof res.data === 'object') {
            this.modelReferenceCounts = res.data;  // 确保引用次数以对象形式加载
          } else {
            ElMessage.error('错误: 无法加载模型引用次数，返回数据格式不正确。');
          }
        })
        .catch(err => {
          console.error('引用次数加载失败:', err);
          ElMessage({
            showClose: true,
            message: '错误: 引用次数加载失败。' + err,
            type: 'error',
          });
        });
    }
  }
};
</script>

<style scoped>
/* 父容器：定义网格布局，使项目卡片能够自适应 */
.m1margin {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); /* 保证卡片在不同屏幕宽度时自适应 */
  grid-gap: 20px; /* 每个项目之间的间距 */
  padding: 20px;
  background-color: #f4f6f9; /* 浅灰色背景 */
  border-radius: 12px; /* 背景也带有圆角，统一风格 */
  height: 100%; /* 父容器占满整个高度 */
}

/* 每个模型卡片的样式 */
.oneItem {
  background-color: #ffffff;
  border-radius: 12px; /* 圆角边框 */
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* 阴影效果，增加立体感 */
  padding: 20px;
  transition: transform 0.3s, box-shadow 0.3s; /* 鼠标悬停时的动画效果 */
  position: relative; /* 为了配合内部元素定位 */
}

/* 鼠标悬停效果，轻微放大和阴影增强 */
.oneItem:hover {
  transform: translateY(-5px); /* 鼠标悬停时卡片上移 */
  box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.15); /* 鼠标悬停时增强阴影 */
}

/* 模型图标 */
.icon {
  width: 80px;
  height: 80px;
  border-radius: 50%; /* 圆形图标 */
  margin-bottom: 20px;
  object-fit: cover; /* 适应图像大小 */
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.15); /* 轻微阴影 */
}

/* 右上角的调用次数样式 */
.rightup {
  background-color: #007bff;
  color: white;
  border-radius: 8px;
  padding: 10px;
  position: absolute;
  top: 15px;
  right: 15px;
  text-align: center;
  font-size: 14px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* 轻微阴影 */
}

/* 模型名称 */
.boldtext {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

/* 普通描述文本 */
.commontext {
  font-size: 16px;
  color: #666;
  margin-bottom: 15px;
}

/* 右下角的开发者信息 */
.rightbottom {
  background-color: #ffce56;
  color: #333;
  font-size: 14px;
  font-weight: bold;
  padding: 8px;
  border-radius: 8px;
  position: absolute;
  bottom: 15px;
  right: 15px;
  text-align: center;
}
</style>