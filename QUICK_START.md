# 🚀 DSE Library - 3分钟快速部署指南

## ✅ 已完成的工作

- ✅ wrangler 安装成功
- ✅ R2 部署系统已就绪
- ✅ 所有脚本已创建
- ✅ 文档已完善

---

## 📋 立即部署（3步完成）

### 第1步: 登录 Cloudflare

```bash
./cloudflare-login.sh
```

浏览器会自动打开，登录你的 Cloudflare 账号。

---

### 第2步: 配置 R2

**2.1 创建 R2 存储桶**
- 访问: https://dash.cloudflare.com/r2
- 点击 "Create bucket"
- 名称: `dselib-papers`
- 选择: Public access

**2.2 获取凭证**
- 在 R2 页面点击 "Manage API tokens"
- 创建 API 令牌（Admin 权限）
- 保存: Access Key ID, Secret Access Key, Account ID

**2.3 编辑配置**
```bash
nano .r2-config
```

填写你的凭证：
```bash
R2_ACCOUNT_ID=你的账户ID
R2_ACCESS_KEY=你的访问密钥
R2_SECRET_KEY=你的密钥
R2_BUCKET_NAME=dselib-papers
R2_PUBLIC_URL=https://pub-xxx.r2.dev  # 创建桶后获得
PAGES_PROJECT_NAME=dselib
```

---

### 第3步: 一键部署

```bash
./deploy-with-r2.sh
```

按提示选择：
- 是否上传 PDF? **y** (首次)
- 是否更新配置? **y** (首次)
- 是否部署 Pages? **y**

**完成！** 访问: `https://dselib.pages.dev`

---

## 🎯 以后更新流程

### 只更新前端代码
```bash
git add .
git commit -m "更新内容"
git push origin main
./deploy-cloudflare-simple.sh
```

### 只上传新 PDF
```bash
./upload-papers-to-r2.sh
```

### 完整更新（代码 + PDF）
```bash
./deploy-with-r2.sh
```

---

## 📁 项目结构

```
dselib/
├── frontend/              # 前端（部署到 Pages）
├── papers/                # PDF文件（上传到 R2）
├── .r2-config            # R2 配置（私有）
├── setup-r2.sh           # R2 配置脚本
├── deploy-with-r2.sh     # 一键部署
├── R2_DEPLOYMENT_GUIDE.md # 详细文档
└── QUICK_START.md        # 本文件
```

---

## 💰 成本

**每月费用:**
- R2 存储 (6.2GB): $0.09
- R2 下载 (1000次): $0.05
- Cloudflare Pages: $0
- **总计: ~$0.14/月**

---

## 🎉 部署成功标志

访问 `https://dselib.pages.dev` 应该看到:
- ✅ 完整的 DSE 试卷浏览界面
- ✅ 所有科目分类正常
- ✅ 搜索功能可用
- ✅ 点击试卷能下载（从 R2）
- ✅ PWA 可安装

---

## 🔗 重要链接

- **在线演示**: https://dselib.pages.dev (部署后)
- **GitHub**: https://github.com/hioTEC/dselib
- **R2 控制台**: https://dash.cloudflare.com/r2
- **详细文档**: `R2_DEPLOYMENT_GUIDE.md`

---

## 🆘 遇到问题？

### wrangler 无法登录
```bash
# 手动登录
wrangler login
```

### AWS CLI 配置失败
```bash
# 手动配置
aws configure set aws_access_key_id "你的密钥"
aws configure set aws_secret_access_key "你的密钥"
aws configure set default.region auto
```

### 上传失败
- 检查 .r2-config 中的凭证是否正确
- 确认 R2 存储桶已创建
- 确认有上传权限

---

## 📝 下一步

1. **现在**: 按照上面的3个步骤部署
2. **部署后**: 测试所有功能
3. **长期**: 享受自动化的部署流程

**祝你部署顺利！** 🎊
