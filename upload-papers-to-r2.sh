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
