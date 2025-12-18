#!/bin/bash

# Cloudflare 登录脚本

echo "🔐 登录 Cloudflare..."

# 使用 npx 运行 wrangler login
npx wrangler login

if [ $? -eq 0 ]; then
    echo "✅ 登录成功！"
    echo "💡 现在可以运行 ./deploy-cloudflare-simple.sh 进行部署"
else
    echo "❌ 登录失败"
fi
