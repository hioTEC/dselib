#!/bin/bash
set -e

echo "🚀 DSE Library 完整部署 (R2 + Cloudflare Pages)"
echo "=================================================="

# 加载配置
if [ -f .r2-config ]; then
    source .r2-config
else
    echo "❌ 错误: 请先运行 ./setup-r2.sh 配置 R2"
    exit 1
fi

# 步骤 1: 上传 PDF 到 R2
echo -e "\n📦 步骤 1: 上传 PDF 到 R2"
read -p "是否上传 PDF 文件? (y/n): " upload_pdf
if [[ $upload_pdf == "y" ]]; then
    ./upload-papers-to-r2.sh
fi

# 步骤 2: 更新前端配置
echo -e "\n⚙️  步骤 2: 更新前端配置"
read -p "是否更新前端 PDF 链接? (y/n): " update_config
if [[ $update_config == "y" ]]; then
    ./update-frontend-config.sh
fi

# 步骤 3: 部署到 Cloudflare Pages
echo -e "\n☁️  步骤 3: 部署到 Cloudflare Pages"
read -p "是否部署到 Cloudflare Pages? (y/n): " deploy_pages
if [[ $deploy_pages == "y" ]]; then
    # 检查是否登录
    if ! wrangler whoami &> /dev/null; then
        echo "需要登录 Cloudflare..."
        wrangler login
    fi
    
    # 部署
    wrangler pages deploy frontend --project-name=$PAGES_PROJECT_NAME
    
    if [ $? -eq 0 ]; then
        echo -e "\n✅ 部署成功！"
        echo "访问: https://$PAGES_PROJECT_NAME.pages.dev"
    else
        echo -e "\n❌ 部署失败"
        exit 1
    fi
fi

echo -e "\n🎉 全部完成！"
