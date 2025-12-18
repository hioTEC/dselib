# 🚀 快速部署到 Cloudflare Pages

## 方法1: 网页上传（推荐，5分钟完成）

1. **打开 Cloudflare Dashboard**
   - 访问: https://dash.cloudflare.com
   - 登录账号

2. **创建 Pages 项目**
   - 进入 "Workers & Pages"
   - 点击 "Create application" → "Pages"
   - 选择 "Upload assets"
   - 项目名称: `dselib`

3. **上传文件**
   - 拖拽整个 `frontend` 文件夹到上传区域
   - 点击 "Save and Deploy"

4. **完成！**
   - 你的网站: `https://dselib.pages.dev`

## 方法2: GitHub 自动部署

1. **推送代码到 GitHub**
   ```bash
   git push origin main
   ```

2. **在 Cloudflare 中连接**
   - 访问: https://dash.cloudflare.com/pages
   - "Create a project" → "Connect to Git"
   - 选择 `hioTEC/dselib` 仓库
   - 配置:
     - Build command: (留空)
     - Build output directory: `frontend`

3. **自动部署**
   - 每次推送代码都会自动更新

## 方法3: 使用 Wrangler（需要 Node.js）

```bash
# 安装
npm install -g wrangler

# 登录
wrangler login

# 部署
wrangler pages deploy frontend --project-name=dselib
```

## ✅ 验证部署

访问: `https://dselib.pages.dev`

应该能看到:
- DSE 试卷浏览界面
- 所有科目分类
- 搜索功能
- PWA 支持

## 📝 重要说明

- **只部署 `frontend` 目录**
- **不包含 `papers/` 文件夹**（PDF文件太大）
- **不包含 `admin/` 工具**
- **自动获得 HTTPS**
- **全球 CDN 加速**

## 🔗 相关链接

- **在线演示**: https://dselib.pages.dev
- **GitHub**: https://github.com/hioTEC/dselib
- **详细文档**: `DEPLOY_TO_CLOUDFLARE.md`
