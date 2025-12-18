#!/bin/bash

# Cloudflare R2 配置脚本

echo "🚀 配置 Cloudflare R2 存储"
echo "=============================="

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. 创建 R2 配置文件
echo -e "${YELLOW}步骤 1: 创建 R2 配置文件${NC}"
cat > .r2-config << 'R2EOF'
# Cloudflare R2 配置
# 在 Cloudflare Dashboard > R2 中创建存储桶和 API 令牌

# 你的 R2 账户 ID
R2_ACCOUNT_ID=your_account_id_here

# R2 访问密钥
R2_ACCESS_KEY=your_access_key_here
R2_SECRET_KEY=your_secret_key_here

# R2 存储桶名称
R2_BUCKET_NAME=dselib-papers

# R2 公共访问 URL (创建存储桶后获得)
R2_PUBLIC_URL=https://pub-xxx.r2.dev

# Cloudflare Pages 项目名称
PAGES_PROJECT_NAME=dselib
R2EOF

echo -e "${GREEN}✓ 已创建 .r2-config 文件${NC}"
echo "请编辑 .r2-config 填入你的 R2 凭证"

# 2. 创建上传脚本
echo -e "\n${YELLOW}步骤 2: 创建 PDF 上传脚本${NC}"
cat > upload-papers-to-r2.sh << 'UPLDEOF'
#!/bin/bash

# 上传 PDF 到 R2 脚本

# 加载配置
source .r2-config

echo "📤 上传 PDF 文件到 R2..."
echo "存储桶: $R2_BUCKET_NAME"
echo "源目录: ./papers/"

# 检查 AWS CLI
if ! command -v aws &> /dev/null; then
    echo "安装 AWS CLI..."
    sudo apt install -y awscli
fi

# 配置 AWS CLI（如果未配置）
if [ ! -f ~/.aws/credentials ]; then
    echo "配置 AWS CLI..."
    aws configure set aws_access_key_id "$R2_ACCESS_KEY"
    aws configure set aws_secret_access_key "$R2_SECRET_KEY"
    aws configure set default.region auto
    aws configure set default.s3.signature_version s3v4
fi

# 上传文件
echo "开始上传..."
aws s3 sync ./papers/ s3://$R2_BUCKET_NAME/ \
  --endpoint-url "https://$R2_ACCOUNT_ID.r2.storage.cloudflarestorage.com" \
  --delete \
  --progress

if [ $? -eq 0 ]; then
    echo -e "\n✅ 上传完成！"
    echo "文件已上传到: s3://$R2_BUCKET_NAME/"
    echo "公共访问: $R2_PUBLIC_URL/papers/"
else
    echo -e "\n❌ 上传失败"
    exit 1
fi
UPLDEOF

chmod +x upload-papers-to-r2.sh
echo -e "${GREEN}✓ 已创建 upload-papers-to-r2.sh${NC}"

# 3. 创建前端配置更新脚本
echo -e "\n${YELLOW}步骤 3: 创建前端配置更新脚本${NC}"
cat > update-frontend-config.sh << 'UPDCFEOF'
#!/bin/bash

# 更新前端 PDF 链接配置

source .r2-config

echo "🔄 更新前端 PDF 链接..."
echo "R2 URL: $R2_PUBLIC_URL"

# 备份原始数据
if [ ! -d "frontend/public/data.backup" ]; then
    echo "创建备份..."
    cp -r frontend/public/data frontend/public/data.backup
fi

# 更新所有 JSON 文件中的 PDF 链接
for json_file in frontend/public/data/*.json; do
    if [ -f "$json_file" ]; then
        # 创建临时文件
        temp_file="${json_file}.tmp"
        
        # 替换 "papers/" 为 R2 URL
        sed "s|\"file\": \"papers/|\"file\": \"$R2_PUBLIC_URL/papers/|g" "$json_file" > "$temp_file"
        
        # 替换成功则覆盖原文件
        if [ $? -eq 0 ]; then
            mv "$temp_file" "$json_file"
            echo "✓ 已更新: $(basename $json_file)"
        else
            rm -f "$temp_file"
            echo "⚠️  跳过: $(basename $json_file)"
        fi
    fi
done

echo -e "\n✅ 所有前端配置已更新！"
echo "现在可以部署到 Cloudflare Pages"
UPDCFEOF

chmod +x update-frontend-config.sh
echo -e "${GREEN}✓ 已创建 update-frontend-config.sh${NC}"

# 4. 创建一键部署脚本
echo -e "\n${YELLOW}步骤 4: 创建完整部署脚本${NC}"
cat > deploy-with-r2.sh << 'DEPFEOF'
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
DEPFEOF

chmod +x deploy-with-r2.sh
echo -e "${GREEN}✓ 已创建 deploy-with-r2.sh${NC}"

# 5. 更新 .gitignore
echo -e "\n${YELLOW}步骤 5: 更新 .gitignore${NC}"
if ! grep -q ".r2-config" .gitignore; then
    echo ".r2-config" >> .gitignore
    echo ".aws" >> .gitignore
    echo "frontend/public/data.backup" >> .gitignore
    echo -e "${GREEN}✓ 已更新 .gitignore${NC}"
fi

echo -e "\n${GREEN}✅ R2 配置完成！${NC}"
echo ""
echo "下一步:"
echo "1. 编辑 .r2-config 填入你的 R2 凭证"
echo "2. 运行: ./deploy-with-r2.sh"
echo ""
echo "创建的脚本:"
echo "  - setup-r2.sh (本脚本)"
echo "  - upload-papers-to-r2.sh (上传 PDF)"
echo "  - update-frontend-config.sh (更新配置)"
echo "  - deploy-with-r2.sh (完整部署)"
