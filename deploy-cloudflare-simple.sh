#!/bin/bash

# Cloudflare Pages 部署脚本 - 使用 npx (无需安装)

echo "🚀 开始部署 DSE Library 到 Cloudflare Pages..."
echo "🔧 使用 npx 运行 wrangler (无需全局安装)"

# 检查前端目录
if [ ! -d "frontend" ]; then
    echo "❌ 错误: frontend 目录不存在"
    exit 1
fi

# 使用 npx 运行 wrangler
echo "☁️ 部署到 Cloudflare Pages..."
npx wrangler pages deploy frontend --project-name=dselib

if [ $? -eq 0 ]; then
    echo "✅ 部署成功！"
    echo "🌐 访问: https://dselib.pages.dev"
else
    echo "❌ 部署失败，请检查错误信息"
    echo "💡 提示: 确保已登录 Cloudflare 账号"
fi
