const express = require("express");
const cors = require("cors");
const fs = require('fs');
const path = require('path');
const multer = require('multer'); // 用于文件上传
const { spawn } = require('child_process'); // 用于运行 Python 处理代码

const app = express();
app.use(cors());
app.use(express.json()); // 用于解析 JSON 请求体

const PORT = 5050;
app.listen(PORT, () => {
  console.log(`正在监听 ${PORT} 端口`);
});

// 获取 __dirname 打印当前的目录，确保路径正确
console.log('__dirname:', __dirname);

// 提供静态文件服务，确保前端能够访问 /data/instance 和 /model 路径
app.use('/data', express.static(path.join(__dirname, 'public', 'data')));
app.use('/model', express.static(path.join(__dirname, 'public', 'model')));
// 配置 Express 静态服务，确保指向 src/uploads 目录
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
console.log('Uploads directory:', path.join(__dirname, 'uploads'));

// 实例列表的路径
const instanceListPath = path.resolve(__dirname, '..', 'public', 'data', 'instance', 'instancelist.json');

// 模型引用次数的路径
const referenceCountPath = path.resolve(__dirname, 'public', 'data', 'modelcallcount.json');

// 动态创建目录
const createDirectoryIfNotExists = (dirPath) => {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
    }
};

// 添加实例的 API
app.post('/addins', (req, res) => {
    const { selectedModel, instanceName, author, notes } = req.body;

    // 读取现有的实例列表
    let instanceList = { data: [] };
    try {
        const data = fs.readFileSync(instanceListPath, 'utf8');
        instanceList = JSON.parse(data);

        if (!instanceList || !Array.isArray(instanceList.data)) {
            instanceList = { data: [] };
        }
    } catch (err) {
        console.error('读取实例列表失败:', err);
        instanceList = { data: [] };
    }

    // 创建新实例对象
    const newInstance = {
        id: instanceList.data.length + 1,  // 自动递增ID
        modelName: selectedModel,
        instanceName,
        creator: author || 'Unauthorized',  // 使用前端提供的作者或默认“匿名”
        time: new Date().toLocaleString(),
        text: notes || '-'
    };

    // 将新实例添加到 data 数组中
    instanceList.data.push(newInstance);

    // 写入到 instancelist.json 文件中
    try {
        fs.writeFileSync(instanceListPath, JSON.stringify(instanceList, null, 2), 'utf8');
        res.json({ message: '实例创建成功', instance: newInstance });
    } catch (err) {
        console.error('写入实例列表失败:', err);
        res.status(500).json({ message: '写入实例列表失败', error: err.toString() });
    }
});

// 处理标准表下载的 API
app.get('/download-standard/:modelId', (req, res) => {
    const modelId = req.params.modelId;
    const standardPath = path.resolve(__dirname, '..', 'public', 'model', modelId, 'standard.xlsx');

    // 打印标准表文件路径
    console.log('Standard filePath:', standardPath);

    // 检查标准表文件是否存在
    if (fs.existsSync(standardPath)) {
        res.download(standardPath, 'standard.xlsx', (err) => {
            if (err) {
                console.error('标准表下载失败:', err);
                res.status(500).send('下载失败');
            }
        });
    } else {
        console.log('标准表未找到:', standardPath);
        res.status(404).send('标准表未找到');
    }
});

// 上传文件并计算的 API
app.post('/upload-and-calculate/:modelId/:instanceId', (req, res) => {
    const { modelId, instanceId } = req.params;
    const uploadDir = path.join(__dirname, 'uploads', modelId, `instance_${instanceId}`);
    const resultDir = path.join(uploadDir, 'result');

    // 创建必要的文件夹
    createDirectoryIfNotExists(uploadDir);
    createDirectoryIfNotExists(resultDir);

    // 设置 multer 的上传目录为实例的文件夹
    const storage = multer.diskStorage({
        destination: (req, file, cb) => {
            cb(null, uploadDir); // 上传文件存储到实例文件夹
        },
        filename: (req, file, cb) => {
            cb(null, 'inputfile.xlsx'); // 将上传文件命名为 inputfile.xlsx
        }
    });

    const upload = multer({ storage }).single('file');

    upload(req, res, (err) => {
        if (err) {
            console.error('上传文件失败:', err);
            return res.status(500).send('文件上传失败');
        }

        const uploadedFilePath = path.join(uploadDir, 'inputfile.xlsx');
        const modelScriptPath = path.join(__dirname, '..', 'public', 'model', modelId, 'model.py');
        const outputFilePath = path.join(resultDir, 'result.xlsx');

        // 打印处理文件的路径，用于调试
        console.log('Uploaded filePath:', uploadedFilePath);
        console.log('Model scriptPath:', modelScriptPath);
        console.log('Output filePath:', outputFilePath);

        // 确保模型的处理脚本存在
        if (!fs.existsSync(modelScriptPath)) {
            return res.status(404).send('处理脚本未找到');
        }

        // 运行 Python 脚本进行处理
        const pythonProcess = spawn('python', [modelScriptPath, uploadedFilePath, outputFilePath]);

        let resultData = ''; // 保存处理结果
        let errorData = '';  // 保存错误信息

        pythonProcess.stdout.on('data', (data) => {
            resultData += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            errorData += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                console.log('处理结果:', resultData);
                // 更新模型引用次数
                updateReferenceCounts(modelId);
                res.send({ message: '文件处理成功', result: resultData });
            } else {
                console.error('处理过程中出错:', errorData);
                res.status(500).send({ message: '文件处理失败', error: errorData });
            }
        });
    });
});

// 处理文件下载的 API
app.get('/uploads/:modelId/instance_:instanceId/result/result.xlsx', (req, res) => {
    const { modelId, instanceId } = req.params;
    const filePath = path.join(__dirname, 'uploads', modelId, `instance_${instanceId}`, 'result', 'result.xlsx');

    // 打印下载路径，检查是否正确
    console.log('Download filePath:', filePath);

    // 检查文件是否存在，然后发送文件
    if (fs.existsSync(filePath)) {
        res.download(filePath, 'result.xlsx');
    } else {
        res.status(404).send('文件未找到');
    }
});

// 更新模型引用次数
const updateReferenceCounts = (modelId) => {
    let referenceCounts = {};
    try {
        const data = fs.readFileSync(referenceCountPath, 'utf8');
        referenceCounts = JSON.parse(data);
    } catch (err) {
        console.error('读取模型引用次数失败，初始化为 0');
        referenceCounts[modelId] = 0;
    }

    if (!referenceCounts[modelId]) {
        referenceCounts[modelId] = 0;
    }

    // 更新模型调用次数
    referenceCounts[modelId] += 1;

    try {
        fs.writeFileSync(referenceCountPath, JSON.stringify(referenceCounts, null, 2), 'utf8');
        console.log(`模型 ${modelId} 的调用次数已更新`);
    } catch (err) {
        console.error('写入引用次数失败:', err);
    }
};

// 模型引用次数统计的 API
app.get('/model/reference-counts', (req, res) => {
    let referenceCounts = {};
    try {
        const data = fs.readFileSync(referenceCountPath, 'utf8');
        referenceCounts = JSON.parse(data);
        res.json(referenceCounts);
    } catch (err) {
        console.error('读取模型引用次数失败:', err);
        res.status(500).send('无法加载引用次数');
    }
});