<template>
    <div>
      <headerline></headerline>
      <div class="mainarea">
        <leftarea ref="leftarea" :chooseModule="choosemodule" :changeModule="changeModule"></leftarea>
        <rightarea ref="rightarea" :chooseModule="choosemodule" :changeModule="changeModule"></rightarea>
      </div>
  
   
      <!-- 实例创建弹窗 -->
      <add-instance @instanceCreated="refreshInstances" v-if="showAddInstance" @close="showAddInstance = false"></add-instance>
    </div>
  </template>
  
  <script>
  import headerline from './HeaderLine'
  import leftarea from './LeftArea'
  import rightarea from './RightArea'
  import AddInstance from './AddInstance'  // 引入 AddInstance 组件
  
  export default {
    name: 'MainWindow',
    components: {
      headerline,
      leftarea,
      rightarea,
      AddInstance
    },
    data() {
      return {
        choosemodule: 2,
        showAddInstance: false,  // 控制弹窗的显示状态
      }
    },
    methods: {
      changeModule(item) {
        this.choosemodule = item;
      },
      // 当实例创建成功后，刷新实例列表
      refreshInstances() {
        console.log("实例创建成功，刷新实例列表...");
        // 调用 leftarea 和 rightarea 的加载实例方法
        this.$refs.leftarea.loadInstances();
        this.$refs.rightarea.loadInstances();
      }
    }
  }
  </script>
  
  <style scoped>
  .mainarea {
    display: flex;
    width: 100%;
    height: 100vh;
  }
  </style>