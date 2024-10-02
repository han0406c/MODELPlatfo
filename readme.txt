已完成部分：
模型库页面，读取本地public/model/modellist.json，用以更新说明文字、LOGO
该model目录下有个test.py测试模型（excel输入到excel输出的模型）

实例页面，读取本地public/data/instance/instancelist.json，用以更新实例列表
下载标准表在public/model/模型名字/standard.xlsx
上传文件会传到public/data/upload，目前是以时间命名
模型运行结果目前设计放在public/data/output，点击计算按钮会自动下载



页面能够自动进行读取模型库、读取实例表、下载标准表
后台服务器是src/server.js，负责创建实例、接受上传文件+启动模型部分



目前欠缺的部分：
1.创建实例界面（目前用旁边的小按钮呼出窗口），需要添加表单内容，并且提交后更新到列表
2.模型库界面，添加统计引用次数
3.项目发布到服务器


运行方式：
页面：终端npm run serve
后台：server.js右键run code