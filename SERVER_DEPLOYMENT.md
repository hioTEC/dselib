# 🖥️ 云服务器部署指南

## 📋 部署选项

你有3种方式使用云服务器：

### 选项1: 仅托管 PDF 文件（推荐）
- 前端：Cloudflare Pages
- PDF：云服务器 + Nginx
- 成本：已有的服务器费用

### 选项2: 完整托管
- 前端 + PDF：云服务器
- 成本：已有的服务器费用

### 选项3: 混合方案
- 前端：Cloudflare Pages
- PDF：云服务器
- 优势：最佳性能 + 成本优化

---

## 🚀 快速部署（选项1 - 推荐）

### 第1步: 准备服务器

```bash
# 登录你的服务器
ssh root@你的服务器IP

# 安装 Nginx
sudo apt update
sudo apt install -y nginx

# 创建目录
sudo mkdir -p /var/www/dselib/papers
sudo chown -R www-data:www-data /var/www/dselib
```

### 第2步: 复制 PDF 文件

**方法A: 使用脚本（推荐）**
```bash
# 在 WSL 中运行
cd /home/hio/dselib
./copy-to-server.sh
# 选择 3) 只复制 PDF 文件
```

**方法B: 手动复制**
```bash
# 在 WSL 中运行
scp -r papers/ root@你的服务器IP:/var/www/dselib/
```

### 第3步: 配置 Nginx

```bash
# 在服务器上创建 Nginx 配置
sudo nano /etc/nginx/sites-available/dselib-papers
```

**配置内容:**
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 或服务器 IP
    
    location /papers/ {
        alias /var/www/dselib/papers/;
        autoindex off;
        
        # CORS 头（允许跨域访问）
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, OPTIONS";
        add_header Access-Control-Allow-Headers "Range";
        
        # 缓存控制
        expires 30d;
        add_header Cache-Control "public, immutable";
        
        # 支持断点续传
        add_header Accept-Ranges bytes;
    }
    
    # 安全：禁止直接访问根目录
    location / {
        return 403;
    }
}
```

**启用配置:**
```bash
sudo ln -s /etc/nginx/sites-available/dselib-papers /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 第4步: 更新前端配置

在 WSL 中运行：
```bash
cd /home/hio/dselib

# 编辑 .r2-config 或直接修改前端 JSON
# 将 PDF 链接指向你的服务器

# 例如，编辑 frontend/public/data/index.json
# 将 "file": "papers/..." 
# 改为 "file": "http://你的服务器IP/papers/..."
```

### 第5步: 部署前端到 Cloudflare Pages

```bash
# 在 WSL 中运行
cd /home/hio/dselib
./deploy-cloudflare-simple.sh
```

---

## 🔒 添加 HTTPS（强烈推荐）

```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo systemctl enable certbot.timer
```

---

## 📊 服务器配置示例

### 完整 Nginx 配置（带 HTTPS）

```nginx
server {
    listen 80;
    server_name papers.dselib.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name papers.dselib.com;
    
    # SSL 证书（Certbot 自动生成）
    ssl_certificate /etc/letsencrypt/live/papers.dselib.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/papers.dselib.com/privkey.pem;
    
    # PDF 文件服务
    location /papers/ {
        alias /var/www/dselib/papers/;
        autoindex off;
        
        # CORS
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, OPTIONS";
        add_header Access-Control-Allow-Headers "Range";
        
        # 缓存
        expires 30d;
        add_header Cache-Control "public, immutable";
        add_header Accept-Ranges bytes;
        
        # 安全头
        add_header X-Content-Type-Options nosniff;
        add_header X-Frame-Options DENY;
    }
    
    # 健康检查
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

---

## 🎯 前端配置更新

### 方法1: 批量更新 JSON 文件

```bash
# 在 WSL 中运行
cd /home/hio/dselib

# 设置服务器 URL
SERVER_URL="http://你的服务器IP"

# 更新所有 JSON 文件
for json_file in frontend/public/data/*.json; do
    sed -i "s|\"file\": \"papers/|\"file\": \"$SERVER_URL/papers/|g" "$json_file"
    echo "已更新: $json_file"
done
```

### 方法2: 手动编辑

编辑 `frontend/public/data/index.json` 和其他 JSON 文件：
```json
{
  "subject": "数学",
  "papers": [
    {
      "year": "2024",
      "file": "http://你的服务器IP/papers/math/2024/p1.pdf"
    }
  ]
}
```

---

## 📦 完整部署流程

### 一次性部署脚本

```bash
#!/bin/bash
# server-deploy.sh

SERVER_IP="你的服务器IP"
SERVER_USER="root"

echo "🚀 开始部署..."

# 1. 上传 PDF
echo "1. 上传 PDF 文件..."
scp -r papers/ $SERVER_USER@$SERVER_IP:/var/www/dselib/

# 2. 配置 Nginx（首次运行）
echo "2. 配置 Nginx..."
ssh $SERVER_USER@$SERVER_IP << 'EOF'
sudo tee /etc/nginx/sites-available/dselib-papers > /dev/null << 'NGINX'
server {
    listen 80;
    server_name your-domain.com;
    
    location /papers/ {
        alias /var/www/dselib/papers/;
        autoindex off;
        add_header Access-Control-Allow-Origin "*";
        add_header Access-Control-Allow-Methods "GET, OPTIONS";
        add_header Access-Control-Allow-Headers "Range";
        expires 30d;
        add_header Cache-Control "public, immutable";
        add_header Accept-Ranges bytes;
    }
    
    location / {
        return 403;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/dselib-papers /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# 3. 部署前端到 Cloudflare Pages
echo "3. 部署前端到 Cloudflare Pages..."
./deploy-cloudflare-simple.sh

echo "✅ 部署完成！"
echo "PDF 服务: http://$SERVER_IP/papers/"
echo "前端: https://dselib.pages.dev"
```

---

## 🎯 推荐方案总结

### 最佳实践

**前端**: Cloudflare Pages
```bash
./deploy-cloudflare-simple.sh
```

**PDF**: 云服务器 + Nginx
```bash
# 1. 上传 PDF
scp -r papers/ root@服务器IP:/var/www/dselib/

# 2. 配置 Nginx（一次性）
# 3. 完成！
```

**成本**: 仅服务器费用（已拥有）  
**性能**: 全球 CDN + 本地高速访问  
**维护**: 简单，只需上传新 PDF

---

## 🔗 相关链接

- **Cloudflare Pages**: https://dash.cloudflare.com/pages
- **项目仓库**: https://github.com/hioTEC/dselib
- **详细文档**: `R2_DEPLOYMENT_GUIDE.md`

---

## 🆘 常见问题

**Q: 无法访问服务器上的 PDF？**
A: 检查 Nginx 配置和防火墙端口（80/443）

**Q: CORS 错误？**
A: 确保 Nginx 配置中有 `Access-Control-Allow-Origin "*"`

**Q: 如何更新 PDF？**
A: 重新运行 `scp -r papers/ root@IP:/var/www/dselib/`

**Q: 想用 HTTPS？**
A: `sudo certbot --nginx -d your-domain.com`

---

## 📝 使用步骤

### 1. 准备服务器（只需一次）
```bash
ssh root@你的服务器IP
sudo apt update && sudo apt install -y nginx
sudo mkdir -p /var/www/dselib/papers
```

### 2. 配置 Nginx（只需一次）
```bash
# 在服务器上创建配置文件
sudo nano /etc/nginx/sites-available/dselib-papers
# 粘贴上面的 Nginx 配置
sudo ln -s /etc/nginx/sites-available/dselib-papers /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

### 3. 上传 PDF（每次更新时）
```bash
# 在 WSL 中
cd /home/hio/dselib
./copy-to-server.sh
# 选择 3) 只复制 PDF 文件
```

### 4. 更新前端配置（只需一次）
```bash
# 在 WSL 中
cd /home/hio/dselib

# 批量更新所有 JSON 文件
SERVER_URL="http://你的服务器IP"
for json_file in frontend/public/data/*.json; do
    sed -i "s|\"file\": \"papers/|\"file\": \"$SERVER_URL/papers/|g" "$json_file"
done
```

### 5. 部署前端（每次更新时）
```bash
./deploy-cloudflare-simple.sh
```

---

## ✅ 验证部署

### 测试 PDF 服务
```bash
# 在浏览器访问
http://你的服务器IP/papers/math/2024/p1.pdf
```

### 测试前端
```bash
# 访问
https://dselib.pages.dev
```

### 检查控制台
- 无 CORS 错误
- PDF 下载正常
- 页面加载快速

---

## 🎉 部署完成！

**现在你的项目:**
- ✅ 前端：Cloudflare Pages（全球 CDN）
- ✅ PDF：云服务器（完全控制）
- ✅ 成本：仅服务器费用
- ✅ 性能：最佳组合

**访问地址:**
- 网站: `https://dselib.pages.dev`
- PDF: `http://你的服务器IP/papers/...`

---

*需要帮助？查看 `QUICK_START.md` 或 `R2_DEPLOYMENT_GUIDE.md`*
