<template>
    <div v-if="visible" class="popup">
      <!-- 弹窗的内容 -->
      <div class="popup-content">
        <!-- 关闭按钮 -->
        <el-button type="primary" class="close-button" @click="closePopup">关闭</el-button>
        <p class="popupheader">请勿关闭操作窗口，计算很快</p>
  
        <!-- 文件选择按钮 -->
        <div class="file-upload-section">
          <el-button type="primary" class="choose-button" @click="triggerFileUpload">选择文件</el-button>
          <input class="filebutton" type="file" style="display: none" ref="fileInput" @change="handleFileUpload">
          <p class="file-text">{{ filename }}</p>
        </div>
  
        <!-- 上传并计算按钮 -->
        <el-button type="primary" class="upload-button" @click="uploadandcalcu(filechosen, usemodel, instanceId)">
          上传并计算
        </el-button>
        
        <!-- 日志显示区域 -->
        <div class="log-container">
          <p class="log-text">{{ responselog }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ElButton, ElMessage } from 'element-plus';
  
  export default {
    name: "PopUp",
    components: {
      ElButton,
    },
    props: {
      visible: {
        type: Boolean,
        default: false,
      },
      content: {
        type: String,
        default: '',
      },
      usemodel: {
        type: String,
        default: '00', // 模型 ID
      },
      instanceId: {
        type: String,
        required: true, // 实例 ID 必须传递
      },
    },
    data() {
      return {
        allowedFileTypes: ['jpg', 'png', 'pdf', 'xlsx'],
        maxFileSize: 5 * 1024 * 1024, // 5MB
        filename: "请选择文件",
        responselog: this.content,
        filechosen: null,
        uploadsucceed: false,
      };
    },
    methods: {
      closePopup() {
        this.$emit('close');
      },
  
      triggerFileUpload() {
        this.$refs.fileInput.click();
      },
  
      handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
  
        const fileType = file.name.split(".").pop().toLowerCase();
        if (!this.allowedFileTypes.includes(fileType)) {
          ElMessage.error("错误: 不支持的文件类型。");
          return;
        }
  
        if (file.size > this.maxFileSize) {
          ElMessage.error(`错误: 文件大小超过 ${this.maxFileSize / (1024 * 1024)}MB 限制。`);
          return;
        }
  
        this.filename = file.name;
        this.filechosen = file;
      },
  
      uploadandcalcu(file, modelId, instanceId) {
        if (!file) {
          ElMessage.error("错误: 未选择文件。");
          return;
        }
  
        const formData = new FormData();
        formData.append('file', file);
  
        // 根据 modelId 和 instanceId 动态生成上传路径
        const url = `http://localhost:5050/upload-and-calculate/${modelId}/${instanceId}`;
  
        axios.post(url, formData)
          .then(response => {
            ElMessage.success("文件上传成功。");
            this.responselog = response.data;
            this.uploadsucceed = true;
            this.downloadresult(modelId, instanceId); // 传递模型和实例 ID 下载结果
          })
          .catch(() => {
            ElMessage.error("文件上传失败。");
            this.uploadsucceed = false;
          });
      },
  
      downloadresult(modelId, instanceId) {
      if (this.uploadsucceed) {
        const url = `http://localhost:5050/uploads/${modelId}/instance_${instanceId}/result/result.xlsx`;
          console.log('Download URL:', url); // 输出生成的下载路径，检查是否正确
          const x = new XMLHttpRequest();
          x.open("GET", url, true);
          x.responseType = "blob";
          x.onload = function () {
              const downloadUrl = window.URL.createObjectURL(x.response);
              const elink = document.createElement("a");
              elink.href = downloadUrl;
              elink.setAttribute("download", 'result.xlsx');
              document.body.appendChild(elink);
              elink.click();
              document.body.removeChild(elink);
          };
          x.send();
      }
    }
    }
  };
  </script>
  
  <style scoped>
  /* 弹窗的背景样式 */
  .popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  /* 弹窗内容 */
  .popup-content {
    background: #fff;
    width: 500px;
    height: auto;
    padding: 20px;
    border-radius: 10px; /* 圆角 */
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* 添加阴影 */
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  /* 关闭按钮 */
  .close-button {
    float: right;
    margin-bottom: 15px;
  }
  
  /* 标题样式 */
  .popupheader {
    text-align: center;
    font-size: 18px; /* 调整字体大小 */
    margin-bottom: 20px;
    color: #333;
  }
  
  /* 文件上传区域 */
  .file-upload-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }
  
  /* 文件名样式 */
  .file-text {
    font-size: 14px;
    color: #555;
    margin-left: 10px;
  }
  
  /* 选择文件按钮样式 */
  .choose-button {
    width: 120px;
    height: 40px;
  }
  
  /* 上传并计算按钮样式 */
  .upload-button {
    width: 150px;
    background-color: #007bff;
    color: white;
    margin: 20px auto;
  }
  
  .upload-button:hover {
    background-color: #0056b3;
  }
  
  /* 日志容器 */
  .log-container {
    margin-top: 20px;
    width: 100%;
    max-height: 150px;
    overflow-y: auto; /* 当内容过多时，允许滚动 */
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 8px; /* 圆角 */
    border: 1px solid #ddd;
  }
  
  /* 日志文本样式 */
  .log-text {
    font-size: 14px;
    color: #333;
    word-wrap: break-word; /* 自动换行 */
  }
  </style>