# DSE Library 中国网络部署方案

## 📊 项目特点分析

- **应用类型**: 纯静态网站（Vue 3 SPA）
- **当前大小**: ~2MB（数据文件）+ PDF文件另计
- **技术栈**: Vue 3 (CDN)、Tailwind CSS (CDN)、Service Worker (PWA)
- **无服务器端**: 不需要Node.js/Python运行环境，只需静态文件托管

---

## 🎯 推荐方案（按性价比排序）

### ⭐ 方案1：Cloudflare Pages（强烈推荐）

**优势**：
- ✅ **完全免费**
- ✅ **中国访问速度快**（有中国大陆节点）
- ✅ **自动HTTPS**
- ✅ **无限流量**（免费计划）
- ✅ **支持自定义域名**
- ✅ **Git集成自动部署**
- ✅ **全球CDN加速**

**部署步骤**：

```bash
# 1. 安装 Wrangler CLI（可选，也可以用网页界面）
npm install -g wrangler

# 2. 登录 Cloudflare
wrangler login

# 3. 部署
wrangler pages deploy frontend --project-name=dselib
```

**或使用网页界面**：
1. 访问 https://dash.cloudflare.com
2. 进入 Pages → Create a project
3. 连接你的 GitHub/GitLab 仓库
4. 设置构建配置：
   - Build command: (留空)
   - Build output directory: `frontend`
5. 点击部署

**访问地址**：`https://dselib.pages.dev`（可绑定自定义域名）

**成本**: **¥0/月**

---

### 🚀 方案2：Vercel（次推荐）

**优势**：
- ✅ **完全免费**（爱好项目）
- ✅ **部署简单**（Git push自动部署）
- ✅ **自动HTTPS**
- ⚠️ 中国访问速度一般（无大陆节点，但可接受）

**部署步骤**：

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 登录并部署
cd d:/CODING/dselib
vercel --prod

# 配置时选择：
# - Build Command: (留空)
# - Output Directory: frontend
```

**或使用网页界面**：
1. 访问 https://vercel.com
2. Import Git Repository
3. 设置 Root Directory: `frontend`
4. 部署

**访问地址**：`https://dselib.vercel.app`

**成本**: **¥0/月**

---

### 💰 方案3：腾讯云静态网站托管（国内优化）

**优势**：
- ✅ **中国访问速度极快**（国内CDN）
- ✅ **价格便宜**
- ✅ **无需备案**（使用云托管域名）
- ⚠️ 需要少量费用

**部署步骤**：

1. 访问 https://console.cloud.tencent.com/tcb
2. 创建环境 → 选择"按量计费"
3. 进入"静态网站托管"
4. 上传文件：

```bash
# 安装 CloudBase CLI
npm install -g @cloudbase/cli

# 登录
tcb login

# 部署
tcb hosting deploy frontend/ -e your-env-id
```

**成本**: 
- 存储：¥0.0043/GB/天（2MB ≈ ¥0.01/月）
- 流量：¥0.18/GB（前5GB免费）
- 总计：**约¥5-10/月**（小流量情况下）

---

### 📦 方案4：阿里云OSS + CDN

**优势**：
- ✅ **稳定可靠**
- ✅ **中国访问快**
- ⚠️ 需要少量费用

**部署步骤**：

```bash
# 1. 安装 ossutil
# 下载：https://help.aliyun.com/document_detail/120075.html

# 2. 配置
./ossutil config

# 3. 上传文件
./ossutil cp -r frontend/ oss://your-bucket-name/ --update

# 4. 开启静态网站托管
./ossutil website oss://your-bucket-name index.html
```

**成本**: 
- 存储：¥0.12/GB/月（2MB ≈ ¥0.01/月）
- 流量：¥0.50/GB（外网流出）
- CDN：¥0.24/GB
- 总计：**约¥10-20/月**（小流量情况下）

---

### 🐙 方案5：GitHub Pages（最简单）

**优势**：
- ✅ **完全免费**
- ✅ **最简单**（push即部署）
- ⚠️ 中国访问速度较慢（无大陆节点）
- ⚠️ 有时会被墙

**部署步骤**：

```bash
# 1. 创建 GitHub 仓库（如果还没有）
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/dselib.git
git push -u origin main

# 2. 配置 GitHub Pages
# 访问仓库 Settings → Pages
# Source: Deploy from a branch
# Branch: main, Folder: /frontend
# 保存

# 或使用 gh-pages 分支
npm install -g gh-pages
gh-pages -d frontend
```

**访问地址**：`https://yourusername.github.io/dselib/`

**成本**: **¥0/月**

---

## 🎬 快速开始：推荐3步部署

### 最快方案（Cloudflare Pages）

```bash
# 1. 注册 Cloudflare 账号（如果没有）
# 访问：https://dash.cloudflare.com/sign-up

# 2. 安装并登录
npm install -g wrangler
wrangler login

# 3. 一键部署
wrangler pages deploy frontend --project-name=dselib
```

完成！你会得到一个 `https://dselib.pages.dev` 地址。

---

## 📝 CDN资源中国优化

你的 `index.html` 使用了这些CDN：
- Vue 3: `unpkg.com`
- Tailwind: `cdn.tailwindcss.com`
- JSZip: `cdnjs.cloudflare.com`
- Font Awesome: `cdnjs.cloudflare.com`

**建议**：替换为国内CDN，提升中国访问速度

### 优化后的CDN（替换方案）

创建 `frontend/index-china.html`，将CDN替换为：

```html
<!-- Vue 3 -->
<script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.prod.js"></script>

<!-- Tailwind (保持不变，或自托管) -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- JSZip -->
<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>

<!-- FileSaver -->
<script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>

<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">

<!-- Google Fonts (可选：自托管) -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
```

**jsdelivr** 在中国有CDN节点，速度很快。

---

## 🔧 部署前优化清单

- [ ] 替换CDN为国内友好的版本（jsdelivr）
- [ ] 压缩JSON数据文件（gzip）
- [ ] 添加 `_headers` 文件（Cloudflare Pages）设置缓存策略
- [ ] 测试PWA功能（Service Worker）
- [ ] 配置自定义域名（可选）

### 添加缓存优化（Cloudflare Pages）

创建 `frontend/_headers` 文件：

```
/public/data/*
  Cache-Control: public, max-age=3600, s-maxage=3600

/*.pdf
  Cache-Control: public, max-age=31536000, immutable

/*.css
  Cache-Control: public, max-age=31536000, immutable

/*.js
  Cache-Control: public, max-age=31536000, immutable

/
  Cache-Control: public, max-age=0, must-revalidate
```

---

## 💡 成本对比总结

| 方案 | 月成本 | 中国速度 | 难度 | 推荐度 |
|------|--------|----------|------|--------|
| Cloudflare Pages | ¥0 | ⭐⭐⭐⭐⭐ | 简单 | ⭐⭐⭐⭐⭐ |
| Vercel | ¥0 | ⭐⭐⭐ | 简单 | ⭐⭐⭐⭐ |
| 腾讯云静态托管 | ¥5-10 | ⭐⭐⭐⭐⭐ | 中等 | ⭐⭐⭐⭐ |
| 阿里云OSS | ¥10-20 | ⭐⭐⭐⭐⭐ | 中等 | ⭐⭐⭐ |
| GitHub Pages | ¥0 | ⭐⭐ | 最简单 | ⭐⭐ |

---

## 🚨 注意事项

### PDF文件存储
如果你的 `papers/` 目录有大量PDF文件：

1. **小于500MB**: 直接部署到Cloudflare Pages（无限制）
2. **大于500MB**: 考虑分离存储
   - PDF放到对象存储（阿里云OSS/腾讯云COS）
   - 前端代码放到Cloudflare Pages
   - 修改 `index.json` 中的PDF路径指向对象存储

### 自动化部署

**推荐**: 使用GitHub Actions自动部署

创建 `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: dselib
          directory: frontend
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

---

## 📞 需要帮助？

如果需要帮助部署，请提供：
1. 你选择的方案（推荐方案1: Cloudflare Pages）
2. 是否需要自定义域名
3. PDF文件总大小

祝部署顺利！🎉
