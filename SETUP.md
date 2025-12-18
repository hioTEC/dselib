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

### Cloudflare Pages (推荐)

**方法1: 使用 npx (WSL兼容)**
```bash
# 直接使用 npx 运行 wrangler
npx wrangler pages deploy frontend --project-name=dselib
```

**方法2: 使用部署脚本**
```bash
# 使用 WSL 兼容的部署脚本
./deploy-cloudflare.sh
```

**方法3: 手动安装 wrangler (原生 Linux)**
```bash
# 安装 Wrangler
npm install -g wrangler

# 登录
wrangler login

# 部署
wrangler pages deploy frontend --project-name=dselib
```

### GitHub Pages

**方法1: 使用部署脚本 (推荐)**
```bash
# 自动部署到 gh-pages 分支
./deploy-github-pages.sh

# 然后在 GitHub 仓库设置中：
# 1. 进入 Settings > Pages
# 2. 选择 gh-pages 分支作为源
# 3. 保存并等待部署
```

**方法2: 使用 Python 脚本**
```bash
# 如果系统有 Python3
python3 deploy-github-pages.py
```

**方法2: 手动部署**
```bash
# 1. 创建 gh-pages 分支
git checkout --orphan gh-pages

# 2. 清理并复制 frontend 内容
git rm -rf .
cp -r frontend/* .

# 3. 添加 .nojekyll 文件
touch .nojekyll

# 4. 提交并推送
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages --force
```

**方法3: 使用 GitHub Actions (自动)**
在仓库根目录创建 `.github/workflows/deploy.yml`：
```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend
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
