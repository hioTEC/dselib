# Cloudflare R2 + Pages 部署指南

## 🎯 架构说明

```
Cloudflare Pages (前端) → Cloudflare R2 (PDF文件)
```

**优势:**
- ✅ 前端全球 CDN 加速
- ✅ PDF 文件专用存储，成本优化
- ✅ 完全控制访问权限
- ✅ 适合大量文件存储

---

## 📋 部署步骤

### 第1步: 创建 Cloudflare R2 存储桶

1. 登录 Cloudflare Dashboard
2. 进入 **R2** 服务
3. 点击 **Create bucket**
4. 设置存储桶名称: `dselib-papers`
5. 选择 **Public access** (允许公共读取)

### 第2步: 生成 R2 API 凭证

1. 在 R2 页面点击 **Manage API tokens**
2. 创建 API 令牌:
   - **Token name**: `dselib-deploy`
   - **Permissions**: **Admin** (需要上传权限)
3. 保存以下信息:
   - Access Key ID
   - Secret Access Key
   - Account ID (在 R2 页面右上角)

### 第3步: 配置 R2 凭证

```bash
# 运行配置脚本
./setup-r2.sh

# 编辑配置文件
nano .r2-config
```

填写你的凭证:
```bash
R2_ACCOUNT_ID=你的账户ID
R2_ACCESS_KEY=你的访问密钥
R2_SECRET_KEY=你的密钥
R2_BUCKET_NAME=dselib-papers
R2_PUBLIC_URL=https://pub-xxx.r2.dev  # 从 R2 设置中获取
PAGES_PROJECT_NAME=dselib
```

### 第4步: 上传 PDF 到 R2

```bash
# 上传所有 PDF 文件
./upload-papers-to-r2.sh
```

**说明:**
- 自动安装 AWS CLI（如果未安装）
- 配置 AWS CLI 凭证
- 同步 `papers/` 目录到 R2
- 支持增量更新

### 第5步: 更新前端配置

```bash
# 更新 JSON 文件中的 PDF 链接
./update-frontend-config.sh
```

**自动执行:**
- 备份原始数据
- 替换所有 `papers/` 链接为 R2 URL
- 保持文件结构不变

### 第6步: 部署到 Cloudflare Pages

```bash
# 完整部署（包含所有步骤）
./deploy-with-r2.sh

# 或者单独部署前端
./deploy-cloudflare-simple.sh
```

---

## 🛠️ 脚本说明

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `setup-r2.sh` | 初始化 R2 配置 | 首次使用 |
| `upload-papers-to-r2.sh` | 上传 PDF 到 R2 | 更新 PDF 时 |
| `update-frontend-config.sh` | 更新前端链接 | 修改 R2 URL 时 |
| `deploy-with-r2.sh` | 完整部署流程 | 一键部署 |

---

## 📊 成本估算

### R2 存储费用
- **存储**: $0.015/GB/月
- **下载**: $0.01/GB
- **免费额度**: 10GB 存储 + 1GB/月下载

**示例:**
- 6.2GB PDF 文件
- 月存储费: ~$0.09
- 1000次下载 (假设每次 5MB): ~$0.05

### Cloudflare Pages
- **免费**: 无限静态文件
- **带宽**: 100GB/月免费
- **构建**: 500次/月免费

**总计**: 每月不到 $0.20

---

## 🔒 安全配置（可选）

### 1. 限制访问来源

在 R2 存储桶设置中:
- **CORS 配置**:
```json
[
  {
    "AllowedOrigins": ["https://dselib.pages.dev"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"]
  }
]
```

### 2. 使用自定义域名

1. 在 Cloudflare 添加域名: `papers.dselib.com`
2. 在 R2 绑定自定义域名
3. 更新前端配置:
```javascript
R2_PUBLIC_URL=https://papers.dselib.com
```

---

## 🎯 完整工作流程

### 日常更新流程

```bash
# 1. 有新 PDF 文件时
./upload-papers-to-r2.sh

# 2. 更新前端代码
git add .
git commit -m "更新内容"
git push origin main

# 3. 部署
./deploy-with-r2.sh
```

### 首次部署流程

```bash
# 1. 安装 wrangler
sudo npm install -g wrangler@latest

# 2. 配置 R2
./setup-r2.sh
# 编辑 .r2-config

# 3. 上传 PDF
./upload-papers-to-r2.sh

# 4. 更新配置
./update-frontend-config.sh

# 5. 部署
./deploy-with-r2.sh
```

---

## 📝 配置文件示例

### .r2-config
```bash
# Cloudflare R2 配置
R2_ACCOUNT_ID=abc123def456
R2_ACCESS_KEY=access_key_here
R2_SECRET_KEY=secret_key_here
R2_BUCKET_NAME=dselib-papers
R2_PUBLIC_URL=https://pub-1234.r2.dev
PAGES_PROJECT_NAME=dselib
```

### 前端配置 (自动更新)
```javascript
// JSON 文件中的链接会自动转换
{
  "file": "https://pub-1234.r2.dev/papers/math/2024/p1.pdf"
}
```

---

## ✅ 验证部署

### 1. 检查 R2 文件
```bash
# 访问 R2 控制台
# 确认文件已上传
```

### 2. 检查前端
```bash
# 访问 https://dselib.pages.dev
# 测试下载功能
```

### 3. 检查控制台
- 无 CORS 错误
- PDF 下载正常
- 页面加载快速

---

## 🎉 部署完成！

**现在你的项目:**
- ✅ 前端在 Cloudflare Pages
- ✅ PDF 在 Cloudflare R2
- ✅ 全球 CDN 加速
- ✅ 成本优化

**访问地址:**
- 网站: `https://dselib.pages.dev`
- PDF: `https://pub-xxx.r2.dev/papers/...`

---

## 🔗 相关链接

- **Cloudflare R2**: https://dash.cloudflare.com/r2
- **Cloudflare Pages**: https://dash.cloudflare.com/pages
- **项目仓库**: https://github.com/hioTEC/dselib

---

*需要帮助？查看 `.r2-config` 文件模板或运行 `./setup-r2.sh` 获取交互式配置*
