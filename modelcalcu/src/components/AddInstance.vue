<template>
  <div v-if="visible" class="popup">
    <div class="popup-content">
      <el-form ref="addInstanceForm" :model="instanceForm" label-width="80px">
        
        <!-- 模型选择 -->
        <el-form-item label="选择模型">
          <el-select v-model="instanceForm.selectedModel" placeholder="请选择模型" size="large" class="custom-select">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>

        <!-- 输入实例名称 -->
        <el-form-item label="实例名称">
          <el-input v-model="instanceForm.instanceName" placeholder="请输入实例名称" class="custom-input"></el-input>
        </el-form-item>

        <!-- 添加作者字段 -->
        <el-form-item label="作者">
          <el-input v-model="instanceForm.author" placeholder="请输入作者名称" class="custom-input"></el-input>
        </el-form-item>

        <!-- 添加备注字段 -->
        <el-form-item label="备注">
          <el-input v-model="instanceForm.notes" placeholder="请输入备注" class="custom-input"></el-input>
        </el-form-item>

        <!-- 提交实例的确认按钮 -->
        <div class="button-group">
          <el-button type="primary" @click="createInstance" class="confirm-button">确认</el-button>
          <el-button type="default" @click="closePopup" class="cancel-button">取消</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  name: "AddInstance",
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      options: [],  // 模型列表选项
      instanceForm: {  // 实例表单数据
        selectedModel: '',
        instanceName: '',
        author: '',  // 新增的作者字段
        notes: ''  // 新增的备注字段
      }
    };
  },
  mounted() {
    this.loadModelList();  // 加载模型列表
  },
  methods: {
    closePopup() {
      this.$emit('close');
    },

    // 加载模型列表
    loadModelList() {
      axios.get('/model/modellist.json')
        .then(res => {
          const modellist = res.data.data;

          if (Array.isArray(modellist)) {
            this.options = modellist.map(model => ({
              value: model.id,
              label: model.name
            }));
          } else {
            ElMessage.error('模型列表格式不正确');
          }
        })
        .catch(() => {
          ElMessage({
            showClose: true,
            message: '错误: 模型载入失败。',
            type: 'error',
          });
        });
    },

    // 提交实例
    createInstance() {
      // 检查必填字段是否填写
      if (!this.instanceForm.selectedModel || !this.instanceForm.instanceName || !this.instanceForm.author) {
        ElMessage.error('请填写所有必填字段');
        return;
      }

      // 打印表单内容以调试
      console.log('提交的实例数据:', this.instanceForm);

      // 发送表单数据到后端
      axios.post('http://localhost:5050/addins', {
        selectedModel: this.instanceForm.selectedModel,
        instanceName: this.instanceForm.instanceName,
        author: this.instanceForm.author,  // 提交作者字段
        notes: this.instanceForm.notes
      })
      .then(() => {
        // 提交成功后的提示信息
        ElMessage({
          showClose: true,
          message: '实例创建成功!',
          type: 'success',
        });

        // 通知父组件刷新实例列表
        this.$emit('instanceCreated');  

        // 关闭弹窗
        this.closePopup();  
      })
      .catch(err => {
        // 错误提示信息
        ElMessage({
          showClose: true,
          message: '实例创建失败: ' + err,
          type: 'error',
        });
        // 打印错误日志
        console.error('实例创建失败:', err);
      });
    }
  }
};
</script>

<style scoped>
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background: #f7f9fc;
  width: 480px;
  height: auto;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
  border: 1px solid #e4e9f0;
}

.custom-input, .custom-select {
  border-radius: 4px;
  border: 1px solid #d1d9e6;
  background-color: #fff;
}

.button-group {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.confirm-button {
  background-color: #5cb85c;
  color: white;
}

.confirm-button:hover {
  background-color: #4cae4c;
}

.cancel-button {
  background-color: #f0f0f0;
  color: #555;
}

.cancel-button:hover {
  background-color: #ddd;
}

.el-form-item {
  margin-bottom: 20px;
}
</style>