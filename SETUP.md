# DSE Library - 项目设置指南

## 📋 项目概述

这是一个香港中学文凭考试（DSE）过往试卷库项目，提供完整的科目试卷资源浏览和下载功能。

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/hioTEC/dselib.git
cd dselib
```

### 2. 本地运行前端

```bash
# 使用Python内置服务器
python -m http.server -d frontend 8000

# 或使用Node.js的http-server
npx http-server frontend -p 8000
```

然后访问: http://localhost:8000

### 3. 管理工具（可选）

```bash
# 安装Python依赖
pip install -r requirements.txt

# 运行索引生成器
cd admin
python indexer.py

# 运行爬虫（需要权限）
python scraper.py

# 运行管理面板
python admin_server.py
```

## 📁 项目结构

```
dselib/
├── frontend/              # 前端应用
│   ├── index.html        # 主页面
│   ├── manifest.json     # PWA配置
│   ├── sw.js            # Service Worker
│   └── public/
│       ├── data/        # JSON索引数据
│       └── downloads/   # PDF文件（生产环境）
├── admin/                # 管理工具
│   ├── indexer.py       # 索引生成器
│   ├── scraper.py       # 爬虫工具
│   └── admin_server.py  # 管理面板
├── papers/              # PDF源文件（开发环境）
├── archive/             # 归档文档
├── requirements.txt     # Python依赖
└── README.md           # 项目说明
```

## 🌐 部署

### Cloudflare Pages

```bash
# 安装Wrangler
npm install -g wrangler

# 登录
wrangler login

# 部署
wrangler pages deploy frontend --project-name=dselib
```

### GitHub Pages

```bash
# 推送到GitHub后，在仓库设置中启用Pages
# 选择 frontend 目录作为发布源
```

## �� 开发

### 前端开发

- **框架**: Vue 3 + Tailwind CSS
- **PWA**: 支持离线访问
- **数据**: JSON索引文件

### 后端工具

- **语言**: Python 3
- **异步**: aiohttp, asyncio
- **数据处理**: BeautifulSoup4

## 📄 许可证

本项目仅用于教育目的，版权归原作者所有。

## 🔗 相关链接

- **在线访问**: https://dselib.pages.dev
- **GitHub**: https://github.com/hioTEC/dselib
