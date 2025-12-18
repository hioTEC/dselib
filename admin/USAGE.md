# DSE Library - 使用说明

## 项目结构

```
dselib/
├── scraper.py          # 异步爬虫脚本
├── indexer.py          # 索引生成器
├── requirements.txt    # Python 依赖
├── downloads/          # 下载的文件存放目录
├── frontend/           # 前端项目 (Vite + Vue 3 + Tailwind)
│   ├── src/
│   │   ├── components/ # Vue 组件
│   │   ├── views/      # 页面视图
│   │   └── ...
│   ├── public/
│   │   ├── data/       # 索引数据 JSON
│   │   ├── robots.txt  # 爬虫规则
│   │   └── ...
│   └── package.json
└── 初步想法.md
```

## 快速开始

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 运行爬虫

```bash
python scraper.py
```

爬虫会自动：
- 异步下载文件（最大5并发）
- 随机延时 0.5-1.5 秒防封
- 自动重试失败请求（最多3次）
- 保存断点状态（可随时中断恢复）
- 记录外部链接（如 Google Drive）

### 3. 生成索引

```bash
python indexer.py
```

索引器会：
- 扫描 `downloads/` 目录
- 智能识别考试类型（DSE/CE/AL）
- 智能识别文件类型（Paper/Marking Scheme等）
- 提取年份信息
- 生成分科目的 JSON 索引
- 生成缺漏报告

### 4. 前端开发

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173 查看效果。

### 5. 构建生产版本

```bash
cd frontend
npm run build
```

构建产物在 `frontend/dist/` 目录。

## 部署

### 静态部署

将以下内容部署到任意静态服务器（GitHub Pages、Vercel、Netlify等）：

1. `frontend/dist/` 目录内容
2. `downloads/` 目录（文件资源）

### 目录结构示例

```
your-server/
├── index.html
├── assets/
├── data/
│   ├── index.json
│   └── subjects/
│       ├── physics.json
│       └── ...
├── downloads/
│   ├── Physics/
│   │   ├── 2024_Paper1.pdf
│   │   └── ...
│   └── ...
└── robots.txt
```

## 功能特性

### 爬虫 (scraper.py)
- ✅ 异步并发下载
- ✅ 随机延时防封
- ✅ 自动重试机制
- ✅ 断点续传
- ✅ 外部链接记录

### 索引器 (indexer.py)
- ✅ 多考试类型支持（DSE/CE/AL/Mock）
- ✅ 智能年份识别（1978-2025）
- ✅ 文件类型分类
- ✅ 分科目 JSON 输出
- ✅ 缺漏报告生成
- ✅ MD5 校验

### 前端
- ✅ Vue 3 + Vite
- ✅ Tailwind CSS
- ✅ 响应式设计
- ✅ PWA 离线支持
- ✅ 搜索功能
- ✅ 分页显示
- ✅ 筛选过滤
- ✅ 深色模式

## 手动补充资源

1. 将文件放入 `downloads/科目名/` 目录
2. 文件名建议包含年份，如 `2024_Paper1.pdf`
3. 重新运行 `python indexer.py`
4. 重新构建前端 `npm run build`

## 注意事项

1. **版权问题**：请遵守相关法律法规
2. **请勿滥用**：爬虫请适度使用，避免对源站造成压力
3. **定期更新**：建议定期运行爬虫更新资源
