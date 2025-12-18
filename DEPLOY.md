# DSE Library 部署指南

## 部署到Linux服务器

这是一个纯静态网站，部署非常简单。

### 方案1：使用Nginx（推荐）

```bash
# 1. 安装nginx
sudo apt update && sudo apt install nginx -y

# 2. 创建网站目录
sudo mkdir -p /var/www/dselib

# 3. 上传frontend目录内容到服务器
# 在本地执行:
rsync -avz --progress frontend/ user@your-server:/var/www/dselib/
# 或使用scp:
scp -r frontend/* user@your-server:/var/www/dselib/

# 4. 创建nginx配置
sudo nano /etc/nginx/sites-available/dselib
```

**Nginx配置内容** (`/etc/nginx/sites-available/dselib`):
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或IP
    root /var/www/dselib;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 开启gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;

    # 静态文件缓存
    location ~* \.(pdf|jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# 5. 启用配置并重启nginx
sudo ln -s /etc/nginx/sites-available/dselib /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 方案2：使用Python简单部署（测试用）

```bash
# 上传文件后，直接运行
cd /path/to/dselib
nohup python3 -m http.server -d frontend 8000 &

# 或使用screen/tmux保持运行
screen -S dselib
python3 -m http.server -d frontend 8000
# 按 Ctrl+A, D 分离
```

### 方案3：使用Caddy（自动HTTPS）

```bash
# 安装Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install caddy

# Caddyfile配置
sudo nano /etc/caddy/Caddyfile
```

**Caddyfile内容**:
```
your-domain.com {
    root * /var/www/dselib
    file_server
    encode gzip
}
```

```bash
sudo systemctl reload caddy
```

## 更新部署

当有新试卷或更新时：

```bash
# 1. 在本地重新运行indexer
python admin/indexer.py

# 2. 同步到服务器
rsync -avz --progress --delete frontend/ user@your-server:/var/www/dselib/
```

## 文件结构说明

部署时只需要 `frontend` 目录：
```
frontend/
├── index.html          # 主页面
├── manifest.json       # PWA清单
├── sw.js              # Service Worker
└── public/
    ├── data/          # 索引数据
    │   ├── index.json
    │   └── subjects/
    └── downloads/     # PDF文件
```

## 注意事项

1. **PDF文件较大**：首次上传可能需要较长时间，建议使用rsync增量同步
2. **权限设置**：确保nginx用户有读取权限 `sudo chown -R www-data:www-data /var/www/dselib`
3. **HTTPS**：生产环境建议配置SSL证书（可用Certbot或Caddy自动获取）
