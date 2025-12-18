# Cloudflare Pages 部署指南

## 🚀 快速部署步骤

### 方法1：使用 Wrangler CLI（推荐）

```bash
# 1. 安装 Wrangler CLI
npm install -g wrangler

# 2. 登录 Cloudflare
wrangler login

# 3. 部署到 Cloudflare Pages
wrangler pages deploy frontend --project-name=dselib

# 4. 访问你的网站
# https://dselib.pages.dev
```

### 方法2：使用 GitHub 集成（自动部署）

1. **推送代码到 GitHub**：
```bash
# 创建 GitHub 仓库（在 GitHub 网站上操作）
# 然后连接远程仓库
git remote add origin https://github.com/你的用户名/dselib.git
git branch -M main
git push -u origin main
```

2. **在 Cloudflare Pages 中连接**：
   1. 访问 https://dash.cloudflare.com/pages
   2. 点击 "Create a project"
   3. 选择 "Connect to Git"
   4. 选择你的 GitHub 仓库
   5. 设置构建配置：
      - Build command: （留空）
      - Build output directory: `frontend`
      - Root directory: `/`
   6. 点击 "Save and Deploy"

### 方法3：使用网页界面直接上传

1. 访问 https://dash.cloudflare.com/pages
2. 点击 "Create a project" → "Upload assets"
3. 拖拽 `frontend` 整个文件夹到上传区域
4. 等待部署完成

---

## 📋 部署前检查清单

- [x] CDN 已优化为 jsdelivr（中国友好）
- [x] 已创建 .gitignore 文件（已排除PDF文件）
- [x] 已提交代码到 Git
- [x] README.md 文件完整
- [ ] 推送到 GitHub 仓库
- [ ] 配置 Cloudflare Pages

## 📦 关于PDF文件

**重要说明**: 为了保持GitHub仓库轻量级，所有PDF文件已被忽略：
- 使用 `git rm -r --cached papers/` 移除了已跟踪的PDF文件
- 在 `.gitignore` 中添加了 `papers/**/*.pdf` 和 `*.pdf` 规则
- 部署时PDF文件需要单独处理（见下文PDF部署方案）

### PDF文件部署方案

由于GitHub有文件大小限制，推荐以下方案：

**方案A: Cloudflare R2存储**
```bash
# 1. 安装 wrangler
npm install -g wrangler

# 2. 上传PDF到R2存储
wrangler r2 put papers/ --recursive

# 3. 在前端代码中使用R2 URL
# 修改 index.json 中的路径为 R2 存储URL
```

**方案B: 分离存储（推荐）**
- 前端代码：GitHub + Cloudflare Pages
- PDF文件：阿里云OSS/腾讯云COS（对象存储）
- 修改索引文件中的PDF路径指向对象存储URL

**方案C: 小规模直接上传**
- 如果PDF总大小 <100MB，可以放到 `frontend/public/downloads/`
- 会包含在GitHub仓库中，但会增加克隆时间

---

## 🔧 配置选项

### 自定义域名（可选）

在 Cloudflare Pages 设置中：
1. 进入你的项目设置
2. 点击 "Custom domains"
3. 添加你的域名（如：dselib.com）
4. 按指示配置 DNS 记录

### 构建设置

```
Framework preset: None
Build command: （留空）
Build output directory: frontend
Root directory: /
Environment variables: 无需设置
```

---

## 📊 监控和日志

部署后，你可以在 Cloudflare Dashboard 中：
- 查看访问统计
- 监控构建日志
- 查看错误信息
- 管理缓存设置

---

## 🎯 部署完成后的网址

- **主网址**: https://dselib.pages.dev
- **预览**: 每次推送会自动创建预览版本
- **回滚**: 支持一键回滚到之前版本

---

## ❓ 常见问题

**Q: 部署后页面显示 404？**
A: 检查 Build output directory 是否设置为 `frontend`

**Q: PDF 文件无法访问？**
A: 确认 papers 目录已正确上传到 frontend/public/downloads

**Q: 在中国访问速度慢？**
A: 已优化 CDN 为 jsdelivr，应该会有明显改善

---

## 📞 获取帮助

如果遇到问题，可以：
1. 查看 Cloudflare Pages 文档
2. 检查构建日志
3. 在 GitHub Issues 中提问

部署完成后，记得更新 README.md 中的网址！
