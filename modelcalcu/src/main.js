import { createApp } from 'vue';

import ElementPlus from 'element-plus';
// import 'element-plus/lib/theme-chalk/index.css';
// //重点 样式必须要加
import 'element-plus/dist/index.css';

import App from './App.vue';
// import EchojoyMessage from './message.js'

const app = createApp(App);
app.use(ElementPlus);
app.mount('#app');
