# DSE Library - 使用说明

## 🚀 快速开始（3分钟部署）

### 1️⃣ 登录 Cloudflare（只需一次）
```bash
./cloudflare-login.sh
```
浏览器会自动打开，登录你的 Cloudflare 账号。

### 2️⃣ 部署网站
```bash
./deploy-cloudflare-simple.sh
```

### 3️⃣ 访问网站
打开: `https://dselib.pages.dev`

**完成！** 🎉

---

## 📋 详细说明

### 项目结构
```
dselib/
├── frontend/              # 前端应用（可部署）
├── admin/                # 管理工具（本地）
├── papers/               # PDF文件（私有，不部署）
├── archive/              # 文档归档
└── 部署脚本和说明文档
```

### 部署脚本

| 脚本 | 说明 | 使用场景 |
|------|------|----------|
| `cloudflare-login.sh` | 登录 Cloudflare | 首次使用 |
| `deploy-cloudflare-simple.sh` | 部署到 Cloudflare Pages | 推荐 |
| `deploy-github-pages.sh` | 部署到 GitHub Pages | 备选方案 |
| `deploy-cloudflare.sh` | 完整部署脚本 | 高级用户 |

### 部署方法对比

| 方法 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **网页上传** | 最简单，无需命令行 | 手动操作 | ⭐⭐⭐⭐⭐ |
| **命令行脚本** | 自动化，可重复 | 需要登录 | ⭐⭐⭐⭐⭐ |
| **GitHub集成** | 自动部署 | 需要GitHub | ⭐⭐⭐⭐ |

### 部署内容说明

**✅ 包含:**
- 主页面 (index.html)
- PWA 配置 (manifest.json)
- Service Worker (sw.js)
- JSON 索引数据 (public/data/)

**❌ 不包含:**
- PDF 文件 (papers/)
- 管理工具 (admin/)
- 文档 (archive/)

### 验证部署

部署成功后，你应该看到:
- ✅ 完整的 DSE 试卷浏览界面
- ✅ 17个科目分类
- ✅ 搜索功能
- ✅ 深色模式切换
- ✅ PWA 安装提示
- ✅ 离线访问支持

### 常见问题

**Q: wrangler 安装失败？**
A: 无需安装！使用 `npx` 自动下载运行。

**Q: 需要 Python 吗？**
A: 不需要，前端是纯 HTML/CSS/JS。

**Q: PDF 文件在哪里？**
A: 部署时不需要 PDF，前端通过 JSON 索引显示数据。

**Q: 如何更新网站？**
A: 修改代码 → 提交 Git → 自动/手动重新部署。

### 相关链接

- **在线演示**: https://dselib.pages.dev
- **GitHub**: https://github.com/hioTEC/dselib
- **详细文档**: `DEPLOYMENT.md`
- **快速指南**: `QUICK_DEPLOY.md`

---

## �� 一句话总结

**运行 `./cloudflare-login.sh` 然后 `./deploy-cloudflare-simple.sh` 即可完成部署！**
