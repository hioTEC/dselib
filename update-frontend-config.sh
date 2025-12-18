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
