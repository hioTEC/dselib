# DSE Library - 香港中学文凭考试过往试卷

一个现代化的香港DSE考试过往试卷浏览和下载平台，提供完整的科目试卷资源。

## 🚀 功能特点

- 📚 **完整科目覆盖** - 涵盖所有DSE科目
- 🔍 **智能搜索** - 快速找到所需试卷
- 📱 **响应式设计** - 支持手机、平板、桌面
- 🌙 **深色模式** - 护眼夜间模式
- 📦 **批量下载** - 支持按年份打包下载
- ⚡ **PWA支持** - 可安装为桌面应用
- 🌏 **中文界面** - 简洁易用的中文界面

## 📊 科目分类

### 核心科目
- 中文
- 英文
- 数学
- 公民与社会发展

### 理科
- 物理
- 化学
- 生物
- 数学延伸M1/M2
- 資訊及通訊科技

### 商科
- 企业、会计与财务概论(BAFS)
- 经济

### 文科
- 中国历史
- 世界历史
- 地理
- 通识教育
- 旅遊與款待

## 🛠️ 技术栈

- **前端**: Vue 3 + Tailwind CSS
- **部署**: Cloudflare Pages (静态托管)
- **PWA**: Service Worker + Web App Manifest
- **数据处理**: Python 索引生成器

## 📁 项目结构

```
dselib/
├── frontend/                 # 前端文件
│   ├── index.html           # 主页面
│   ├── manifest.json        # PWA配置
│   ├── sw.js              # Service Worker
│   └── public/            # 静态资源
│       ├── data/           # 索引数据
│       └── downloads/     # PDF文件（生产环境）
├── admin/                  # 管理工具
│   ├── indexer.py         # 索引生成器
│   ├── scraper.py         # 数据抓取工具
│   └── admin_server.py    # 本地管理界面
├── papers/                # 源PDF文件（开发环境）
└── DEPLOYMENT_CHINA.md    # 部署指南
```

## 🚀 快速开始

### 本地运行

```bash
# 克隆仓库
git clone https://github.com/yourusername/dselib.git
cd dselib

# 运行本地服务器（Python 3）
python -m http.server -d frontend 8000

# 打开浏览器
open http://localhost:8000
```

### 重新生成索引

```bash
cd admin
python indexer.py
```

## 🌐 在线访问

- **主站**: https://dselib.pages.dev
- **GitHub**: https://github.com/yourusername/dselib

## 📄 许可证

本项目仅用于教育目的，版权归原作者所有。

---

⭐ 如果这个项目对你有帮助，请给个Star！
