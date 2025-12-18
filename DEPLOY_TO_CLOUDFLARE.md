# Cloudflare Pages 部署指南

## 🚀 快速部署（推荐方法）

### 方法1: 使用 Cloudflare 网页界面（最简单）

1. **准备前端文件**
   ```bash
   cd /home/hio/dselib
   # frontend 目录已经包含了所有需要的文件
   ```

2. **登录 Cloudflare Dashboard**
   - 访问 https://dash.cloudflare.com
   - 登录你的账号

3. **创建 Pages 项目**
   - 进入 "Workers & Pages"
   - 点击 "Create application" → "Pages"
   - 选择 "Upload assets"
   - 项目名称: `dselib`
   - 拖拽 `frontend` 文件夹到上传区域
   - 点击 "Save and Deploy"

4. **访问你的网站**
   - 部署完成后，访问: `https://dselib.pages.dev`

### 方法2: 使用 GitHub 集成（自动部署）

1. **推送代码到 GitHub**
   ```bash
   git push origin main
   ```

2. **在 Cloudflare 中连接 GitHub**
   - 访问 https://dash.cloudflare.com/pages
   - 点击 "Create a project" → "Connect to Git"
   - 选择 `hioTEC/dselib` 仓库
   - 配置:
     - Build command: (留空)
     - Build output directory: `frontend`
   - 点击 "Save and Deploy"

3. **自动部署**
   - 之后每次推送代码都会自动部署

### 方法3: 使用 Wrangler CLI（需要安装）

```bash
# 安装 Wrangler
npm install -g wrangler

# 登录
wrangler login

# 部署
wrangler pages deploy frontend --project-name=dselib
```

## 📁 部署内容说明

**只部署前端部分:**
- ✅ `frontend/index.html` - 主页面
- ✅ `frontend/manifest.json` - PWA 配置
- ✅ `frontend/sw.js` - Service Worker
- ✅ `frontend/public/data/` - JSON 索引数据
- ✅ `frontend/public/downloads/` - PDF 文件（可选）

**不部署:**
- ❌ `papers/` - 源PDF文件（太大，私有）
- ❌ `admin/` - 管理工具
- ❌ `archive/` - 文档

## 🔧 部署后配置

### 启用自定义域名（可选）
1. 在 Cloudflare Dashboard 中
2. 进入 Pages 项目设置
3. 添加自定义域名
4. 按照提示配置 DNS

### 检查部署状态
- 访问: https://dselib.pages.dev
- 检查浏览器控制台是否有错误
- 测试 PWA 功能

## 📝 注意事项

- **PDF 文件**: 如果 `frontend/public/downloads/` 包含大量 PDF，建议只部署 `data/` 目录
- **缓存**: Cloudflare 会自动缓存静态文件
- **HTTPS**: 自动启用
- **CDN**: 全球加速

## 🎯 成功标志

部署成功后，你应该能看到:
- 完整的 DSE 试卷浏览界面
- 所有科目分类
- 搜索功能
- PWA 安装提示
- 离线访问支持
