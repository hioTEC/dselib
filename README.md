# DSE Library - 香港中学文凭考试过往试卷

一个现代化的香港DSE考试过往试卷浏览和下载平台，提供完整的科目试卷资源。

## 🚀 功能特点

- 📚 **完整科目覆盖** - 涵盖所有DSE科目
- 🔍 **智能搜索** - 快速找到所需试卷
- 📱 **响应式设计** - 支持手机、平板、桌面
- 🌙 **深色模式** - 护眼夜间模式
- 📦 **批量下载** - 支持按年份打包下载
- ⚡ **PWA支持** - 可安装为桌面应用
- 🌏 **中文界面** - 简洁易用的中文界面
- 🔒 **HTTPS支持** - 自动获取Let's Encrypt证书

## 📊 科目分类

### 核心科目
- 中文
- 英文
- 数学
- 公民与社会发展

### 理科
- 物理
- 化学
- 生物
- 数学延伸M1/M2
- 資訊及通訊科技

### 商科
- 企业、会计与财务概论(BAFS)
- 经济

### 文科
- 中国历史
- 世界历史
- 地理
- 通识教育
- 旅遊與款待

## 🛠️ 技术栈

- **前端**: Vue 3 + Tailwind CSS
- **Web服务器**: Caddy (自动HTTPS)
- **PWA**: Service Worker + Web App Manifest
- **数据处理**: Python 索引生成器

## 📁 项目结构

```
/var/www/dselib/            # 生产环境
├── index.html              # 主页面
├── manifest.json           # PWA配置
├── sw.js                   # Service Worker
└── public/                 # 静态资源
    ├── data/               # 索引数据
    └── downloads/          # 试卷PDF文件

/root/dselib/               # 开发环境
├── frontend/               # 前端源文件
│   ├── index.html
│   ├── manifest.json
│   ├── sw.js
│   └── public/
│       ├── data/          # 索引数据（自动生成）
│       └── sources/       # 试卷源文件
│           └── {科目}/{考试类型}/{语言}/{年份}/
├── admin/                  # 管理工具
│   ├── maintain.py        # 维护脚本（推荐）
│   ├── subject_config.json # 科目配置
│   ├── indexer.py         # 旧版索引生成器
│   ├── scraper.py         # 数据抓取工具
│   └── admin_server.py    # 管理界面
└── README.md              # 本文件
```

## 🚀 部署说明

### 自动部署

```bash
# 生成索引并同步到生产环境（推荐）
python3 admin/maintain.py
```

### 手动同步

```bash
# 同步所有文件
cp -r frontend/* /var/www/dselib/
```

### 服务管理

```bash
# 查看服务状态
systemctl status caddy

# 重启服务
systemctl restart caddy

# 查看日志
journalctl -u caddy -f
```

## 🛠️ 管理工具

### 维护脚本 (推荐)

```bash
# 生成索引并同步到生产环境
python3 admin/maintain.py

# 只生成索引
python3 admin/maintain.py index

# 只同步到生产环境
python3 admin/maintain.py sync

# 生成索引并同步
python3 admin/maintain.py all
```

### 添加新试卷

1. 将PDF文件放入 `frontend/public/sources/` 对应目录
2. 目录结构：`{科目}/{考试类型}/{语言}/{年份}/文件.pdf`
3. 运行维护脚本自动生成索引

**示例**：
```bash
# 添加物理2025年中文卷
frontend/public/sources/phy/dse/chi/2025/p1.pdf

# 添加新考试类型
frontend/public/sources/phy/新考试局/chi/2025/p1.pdf
```

### 其他工具

```bash
# 数据抓取
cd admin
python scraper.py

# 启动管理界面
cd admin
python admin_server.py
```

## 🔒 HTTPS证书

Caddy会自动管理Let's Encrypt证书：
- 自动申请证书
- 自动续期（到期前30天）
- 自动重定向HTTP到HTTPS

证书存储在：`/var/lib/caddy/.local/share/caddy/certificates/`

## 📝 配置文件

### Caddy配置

位置：`/etc/caddy/Caddyfile`

```caddyfile
dselib.hiotec.com {
    root * /var/www/dselib
    file_server
    encode gzip
    
    # 静态资源缓存
    @static {
        path *.css *.js *.png *.jpg *.jpeg *.gif *.ico *.svg *.woff *.woff2 *.ttf *.eot
    }
    handle @static {
        header Cache-Control "public, max-age=31536000"
    }
    
    # SPA路由支持
    try_files {path} {path}/index.html
    
    # 安全头
    header {
        -Server
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        X-XSS-Protection "1; mode=block"
        Referrer-Policy strict-origin-when-cross-origin
    }
    
    # 自动HTTPS
    tls {
        protocols tls1.2 tls1.3
        ciphers TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 
                TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 
                TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 
                TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 
                TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 
                TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256
    }
}
```

## 🌐 访问方式

- **域名**: dselib.hiotec.com
- **HTTP**: 自动重定向到HTTPS
- **HTTPS**: https://dselib.hiotec.com
- **协议**: 支持HTTP/1.1, HTTP/2, HTTP/3

## 📦 Python环境

```bash
# 激活环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 🔄 维护命令

```bash

# 检查服务状态
systemctl status caddy

# 查看Caddy日志
journalctl -u caddy --no-pager

# 测试HTTPS连接
curl -k https://localhost
```

## 📄 许可证

本项目仅用于教育目的，版权归原作者所有。

---

✅ 项目已成功部署并运行中！
