# DSE Library - 部署完整指南

## 🎯 推荐部署流程（3步完成）

### 第1步: 登录 Cloudflare（只需一次）
```bash
./cloudflare-login.sh
```
浏览器会自动打开，按提示登录 Cloudflare 账号。

### 第2步: 选择部署方法

**方法A: 网页上传（最简单，无需命令行）**
1. 访问 https://dash.cloudflare.com
2. Workers & Pages → Create → Pages → Upload assets
3. 拖拽 `frontend` 文件夹
4. 完成！

**方法B: 命令行部署（推荐开发者）**
```bash
./deploy-cloudflare-simple.sh
```

**方法C: GitHub 自动部署**
1. 推送代码到 GitHub
2. 在 Cloudflare Pages 连接 GitHub 仓库
3. 设置构建目录为 `frontend`
4. 之后自动部署

### 第3步: 访问网站
部署完成后访问: `https://dselib.pages.dev`

## 📁 部署内容

**包含:**
- ✅ `frontend/index.html` - 主页面
- ✅ `frontend/manifest.json` - PWA 配置
- ✅ `frontend/sw.js` - Service Worker
- ✅ `frontend/public/data/` - JSON索引数据

**不包含:**
- ❌ `papers/` - PDF源文件（6.2GB，私有）
- ❌ `admin/` - 管理工具
- ❌ `archive/` - 文档

## 🔧 脚本说明

| 脚本 | 用途 |
|------|------|
| `cloudflare-login.sh` | 登录 Cloudflare（只需一次） |
| `deploy-cloudflare-simple.sh` | 部署到 Cloudflare Pages |
| `deploy-github-pages.sh` | 部署到 GitHub Pages |
| `deploy.sh` | 原始部署脚本 |

## 📝 注意事项

1. **无需安装 wrangler** - 使用 npx 自动下载
2. **PDF 文件** - 不包含在部署中（保持轻量）
3. **自动 HTTPS** - Cloudflare 自动提供
4. **全球 CDN** - 自动加速
5. **PWA 支持** - 可安装为桌面应用

## ✅ 验证部署

部署成功后检查:
- ✅ 网站可访问
- ✅ 所有科目显示正常
- ✅ 搜索功能工作
- ✅ PWA 可安装
- ✅ 离线访问可用

## 🚀 开始部署

```bash
# 1. 登录（只需一次）
./cloudflare-login.sh

# 2. 部署
./deploy-cloudflare-simple.sh

# 3. 访问
# 打开 https://dselib.pages.dev
```

**就这么简单！** 🎉
