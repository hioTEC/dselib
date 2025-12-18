# 🚀 如何部署 DSE Library

## ⚡ 3分钟快速开始

### 方案A: Cloudflare R2 + Pages (推荐，成本最低)

```bash
# 1. 登录 Cloudflare
./cloudflare-login.sh

# 2. 配置 R2
./setup-r2.sh
# 编辑 .r2-config 填入 R2 凭证

# 3. 一键部署
./deploy-with-r2.sh
```

**成本**: $0.14/月  
**访问**: `https://dselib.pages.dev`

---

### 方案B: 云服务器 + Cloudflare Pages (已有服务器)

```bash
# 1. 准备服务器（只需一次）
ssh root@你的服务器IP
sudo apt install -y nginx
sudo mkdir -p /var/www/dselib/papers

# 2. 配置 Nginx（只需一次）
# 复制 SERVER_DEPLOYMENT.md 中的 Nginx 配置

# 3. 上传 PDF
./copy-to-server.sh
# 选择 3) 只复制 PDF 文件

# 4. 更新前端配置
# 编辑 JSON 文件，将 PDF 链接改为服务器 URL

# 5. 部署前端
./deploy-cloudflare-simple.sh
```

**成本**: 已有服务器费用  
**访问**: `https://dselib.pages.dev` + `http://服务器IP/papers/`

---

### 方案C: 网页上传 (最简单，无需命令行)

1. 访问 https://dash.cloudflare.com
2. Workers & Pages → Create → Pages → Upload assets
3. 拖拽 `frontend` 文件夹
4. 完成！

**成本**: $0  
**访问**: `https://dselib.pages.dev`

---

## 📚 详细文档

| 文档 | 用途 |
|------|------|
| `QUICK_START.md` | 3分钟快速开始 |
| `R2_DEPLOYMENT_GUIDE.md` | R2 详细指南 |
| `SERVER_DEPLOYMENT.md` | 服务器部署 |
| `USAGE.md` | 日常使用说明 |

---

## 🎯 我该选哪个？

**如果你有云服务器:**
→ 选择 **方案B** (服务器 + Pages)

**如果你想要最低成本:**
→ 选择 **方案A** (R2 + Pages)

**如果你想要最简单:**
→ 选择 **方案C** (网页上传)

---

## ✅ 部署后验证

访问 `https://dselib.pages.dev` 检查:
- [ ] 所有科目显示正常
- [ ] 搜索功能可用
- [ ] PDF 可以下载
- [ ] 深色模式正常
- [ ] PWA 可安装

---

## 🆘 遇到问题？

**wrangler 登录问题:**
```bash
wrangler login
```

**R2 配置问题:**
```bash
./setup-r2.sh
# 检查 .r2-config 文件
```

**服务器连接问题:**
```bash
# 测试 SSH
ssh root@你的服务器IP

# 测试 Nginx
curl -I http://你的服务器IP/papers/
```

---

## 🎉 开始部署

**现在就去:**
1. 阅读 `QUICK_START.md`
2. 选择一个方案
3. 运行脚本
4. 享受你的网站！

**祝你部署顺利！** 🚀
