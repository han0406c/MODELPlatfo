<template>
  <div class="module-container">
    <div class="button-container">
      <!-- 操作按钮 -->
      <button class="thebutton" @click="showAddins">创建实例</button>
    </div>

    <!-- 弹窗用于创建实例 -->
    <Addins :visible="addinsVisible" @close="closeAddins" @instanceCreated="refreshTable" />

    <!-- 表格展示实例 -->
    <div class="table-container">
      <table class="m2table">
        <thead>
          <tr>
            <th>序号</th>
            <th>引用模型</th>
            <th>实例名称</th>
            <th>作者</th>
            <th>创建时间</th>
            <th>备注</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in sortedTableData" :key="index">
            <td>{{ item.id }}</td>
            <td>{{ item.modelName }}</td>
            <td>{{ item.instanceName }}</td>
            <td>{{ item.creator }}</td>
            <td>{{ item.time }}</td>
            <td>{{ item.text }}</td>
            <td>
              <button class="action-button" @click="downloadstd(item.modelName)">下载标准表</button>
              <button class="action-button" @click="showPopup(item.modelName, item.id)">计算</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 计算弹窗，传递模型ID和实例ID -->
    <Popup 
      :visible="popupVisible" 
      :content="popupContent" 
      :usemodel="popupUseModel" 
      :instanceId="popupInstanceId" 
      @close="closePopup" 
    />
  </div>
</template>

<script>
  import Popup from './Popup.vue';
  import Addins from './AddInstance.vue';
  import axios from 'axios';
  import { ElMessage } from 'element-plus';

  export default {
    name: 'ModuleTwo',
    components: {
      Popup,
      Addins,
    },
    data() {
      return {
        popupVisible: false,
        popupContent: '这是一个log',
        popupUseModel: '00',       // 用于存储模型ID
        popupInstanceId: null,     // 用于存储实例ID
        addinsVisible: false,
        tableData: [],             // 初始为空
      };
    },
    mounted() {
      this.loadinginstance();      // 初始化时加载实例列表
    },
    methods: {
      showPopup(modelId, instanceId) {
        this.popupUseModel = modelId;     // 设置模型ID
        this.popupInstanceId = instanceId; // 设置实例ID
        this.popupVisible = true;
      },
      closePopup() {
        this.popupVisible = false;
      },
      showAddins() {
        this.addinsVisible = true;
      },
      closeAddins() {
        this.addinsVisible = false;
      },
      // 动态生成标准表的下载链接
      downloadstd(modelName) {
        const url = `/model/${modelName}/standard.xlsx`;
        const x = new XMLHttpRequest();
        x.open('GET', url, true);
        x.responseType = 'blob';
        x.onload = function () {
          const downloadUrl = window.URL.createObjectURL(x.response);
          const elink = document.createElement('a');
          elink.href = downloadUrl;
          elink.target = '_self';
          elink.setAttribute('download', 'standard.xlsx');
          elink.style.display = 'none';
          document.body.appendChild(elink);
          elink.click();
          document.body.removeChild(elink);
        };
        x.send();
      },

      // 加载实例列表
      loadinginstance() {
        axios
          .get('/data/instance/instancelist.json')
          .then((res) => {
            this.tableData = res.data.data;
            this.sortTableData();  // 调用排序方法，确保实例顺序正确
          })
          .catch((err) => {
            console.log('实例载入失败:', err);
            ElMessage({
              showClose: true,
              message: '错误: 实例载入失败。',
              type: 'error',
            });
          });
      },

      // 刷新表格数据
      refreshTable() {
        this.loadinginstance(); // 重新加载实例列表
        ElMessage({
          showClose: true,
          message: '实例列表已更新。',
          type: 'success',
        });
      },

      // 根据 id 或 time 进行排序
      sortTableData() {
        this.tableData.sort((a, b) => b.id - a.id); // id 越大，位置越靠前
      }
    },
    computed: {
      sortedTableData() {
        return this.tableData;
      }
    }
  };
</script>

<style scoped>
  /* 主容器样式 */
  .module-container {
    padding: 20px;
    background-color: #f9fafb;
    min-height: 100vh;
  }

  /* 按钮容器 */
  .button-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
  }

  /* 操作按钮样式 */
  .thebutton {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    margin-left: 10px;
  }

  .thebutton:hover {
    background-color: #0056b3;
    transform: translateY(-3px);
  }

  /* 表格容器样式 */
  .table-container {
    width: 100%;
    overflow-x: auto;
  }

  /* 表格样式 */
  .m2table {
    width: 100%;
    border-collapse: collapse;
    background-color: #ffffff;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }

  .m2table th,
  .m2table td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
  }

  .m2table th {
    background-color: #f4f6f9;
    font-size: 16px;
    font-weight: bold;
  }

  .m2table td {
    font-size: 14px;
    color: #555;
  }

  /* 操作按钮（下载标准表和计算） */
  .action-button {
    background-color: #68946c;
    color: white;
    padding: 6px 12px;
    border: none;
    border-radius: 3px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    margin-right: 10px;
  }

  .action-button:hover {
    background-color: #ff664b;
    transform: translateY(-2px);
  }
</style>