#!/bin/bash

# DSE Library 部署脚本

echo "🚀 开始部署 DSE Library..."

# 检查是否安装了 Wrangler
if ! command -v wrangler &> /dev/null; then
    echo "📦 安装 Wrangler..."
    npm install -g wrangler
fi

# 登录 Cloudflare (如果未登录)
echo "🔐 登录 Cloudflare..."
wrangler login

# 部署到 Cloudflare Pages
echo "☁️ 部署到 Cloudflare Pages..."
wrangler pages deploy frontend --project-name=dselib

echo "✅ 部署完成！"
echo "🌐 访问: https://dselib.pages.dev"
