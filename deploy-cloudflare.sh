#!/bin/bash

# Cloudflare Pages 部署脚本 (WSL兼容版本)

echo "🚀 开始部署 DSE Library 到 Cloudflare Pages..."

# 检查是否在WSL中
if grep -qEi "(Microsoft|WSL)" /proc/version &>/dev/null; then
    echo "🔧 检测到 WSL 环境，使用 npx 运行 wrangler..."
    
    # 使用 npx 运行 wrangler (避免平台兼容性问题)
    npx wrangler pages deploy frontend --project-name=dselib
    
else
    # 原生 Linux 环境
    echo "🔧 检测到原生 Linux 环境..."
    
    # 检查是否安装了 wrangler
    if ! command -v wrangler &> /dev/null; then
        echo "📦 安装 wrangler..."
        npm install -g wrangler
    fi
    
    # 登录 (如果需要)
    echo "🔐 登录 Cloudflare..."
    wrangler login
    
    # 部署
    echo "☁️ 部署到 Cloudflare Pages..."
    wrangler pages deploy frontend --project-name=dselib
fi

echo "✅ 部署完成！"
echo "🌐 访问: https://dselib.pages.dev"
