# 🚀 在 Open WebUI 界面中调用本地 GraphRAG

## 📖 简介

这个指南将帮助您在 Open WebUI 的网页界面中直接调用本地的 GraphRAG，无需使用终端命令。

## 🎯 实现目标

- ✅ 通过 Open WebUI 网页界面调用 GraphRAG
- ✅ 支持本地搜索和全局搜索
- ✅ 实时状态显示
- ✅ 中文友好的操作界面

## 📋 操作步骤

### 1. 打开 Open WebUI 管理界面

1. **确保 Open WebUI 正在运行**
   ```bash
   open-webui serve
   ```

2. **打开浏览器访问**: `http://localhost:8080`

3. **登录管理员账户**

### 2. 添加 GraphRAG 功能

1. **进入管理面板**:
   - 点击右上角头像
   - 选择 "Admin Panel"
   - 点击 "Functions" 标签

2. **创建新功能**:
   - 点击 "Create Function" 按钮
   - 填写以下信息：
     - **Function ID**: `graphrag_local`
     - **Name**: `GraphRAG 本地调用`
     - **Description**: `通过界面调用本地 GraphRAG 进行知识图谱搜索`

3. **复制功能代码**:
   将 `graphrag_chinese_function.py` 文件中的全部代码复制到代码框中

4. **保存并启用**:
   - 点击 "Save" 保存
   - 切换开关启用功能
   - 设置为 "Global" 以便所有用户使用

### 3. 使用 GraphRAG 功能

返回聊天界面，您可以使用以下命令：

#### 🔍 本地搜索（适合具体问题）
```
@graphrag_local_search 斯克鲁奇是什么样的人物？
```

#### 🌍 全局搜索（适合主题分析）
```
@graphrag_global_search 这个故事的主要主题是什么？
```

#### 📊 检查状态
```
@graphrag_status
```

#### 🚀 运行索引（如果需要）
```
@graphrag_index
```

## 🎨 界面效果

使用这些功能时，您会看到：

- 🔍 **实时搜索状态**: "正在使用 GraphRAG 搜索..."
- 📊 **进度提示**: "执行 local 搜索中..."
- ✅ **完成通知**: "GraphRAG 搜索完成"
- 📋 **格式化结果**: 清晰的搜索结果展示

## 💡 使用示例

### 示例 1: 角色分析
**输入**: `@graphrag_local_search 斯克鲁奇的性格特点`

**输出**: 详细的角色分析，包括性格特征、转变过程等

### 示例 2: 主题探索
**输入**: `@graphrag_global_search 圣诞节的象征意义`

**输出**: 关于圣诞节主题的全面分析

### 示例 3: 状态检查
**输入**: `@graphrag_status`

**输出**: 
```
📊 GraphRAG 状态检查

✅ GraphRAG 仓库已找到
✅ 虚拟环境已找到
✅ 数据目录已找到
📁 输入文件: 1 个文档
   - book.txt
📊 已有索引数据，可以进行搜索
```

## 🔧 配置说明

功能会自动检测以下路径：
- **GraphRAG 仓库**: `~/Developments/simulation/graphrag`
- **数据目录**: `~/Developments/simulation/graphrag/ragtest`
- **虚拟环境**: `~/Developments/simulation/graphrag/.venv`

如需修改路径，可以编辑功能代码中的路径配置。

## 🎉 优势

通过这种方式，您可以：

- 🖱️ **通过点击和输入使用 GraphRAG**，无需记忆命令行
- 👥 **与团队共享**，其他用户也可以通过界面使用
- 🔄 **与 AI 对话结合**，搜索结果可以作为对话上下文
- 📱 **移动端友好**，在手机上也可以使用
- 📊 **实时反馈**，清楚知道搜索进度

## 🚀 完成！

现在您已经成功将 GraphRAG 集成到 Open WebUI 界面中了！可以通过简单的 `@` 命令调用本地 GraphRAG 功能，享受图形化界面带来的便利。
