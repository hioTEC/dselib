#!/bin/bash

# 快速复制到服务器

echo "📤 复制 DSE Library 到服务器"
echo "=============================="

# ⚠️ 请先修改下面的配置
SERVER_USER="root"              # 你的服务器用户名
SERVER_IP="192.168.1.100"       # 你的服务器 IP
SERVER_PATH="/var/www/dselib"   # 服务器路径

# 检查是否已配置
if [ "$SERVER_IP" = "192.168.1.100" ]; then
    echo "❌ 请编辑脚本，配置你的服务器信息！"
    echo ""
    echo "修改这些变量:"
    echo "  SERVER_USER=\"$SERVER_USER\""
    echo "  SERVER_IP=\"$SERVER_IP\""
    echo "  SERVER_PATH=\"$SERVER_PATH\""
    exit 1
fi

echo "服务器: $SERVER_USER@$SERVER_IP"
echo "目标路径: $SERVER_PATH"
echo ""

# 选择复制模式
echo "请选择复制模式:"
echo "1) 只复制 frontend (推荐，用于部署)"
echo "2) 复制全部文件"
echo "3) 只复制 PDF 文件到服务器"
read -p "选择 (1/2/3): " choice

case $choice in
    1)
        echo "复制 frontend/..."
        scp -r frontend/ $SERVER_USER@$SERVER_IP:$SERVER_PATH/
        echo "✅ 完成！"
        echo ""
        echo "在服务器上运行:"
        echo "  cd $SERVER_PATH/frontend"
        echo "  python3 -m http.server 8000"
        ;;
    2)
        echo "复制全部文件..."
        scp -r . $SERVER_USER@$SERVER_IP:$SERVER_PATH/
        echo "✅ 完成！"
        ;;
    3)
        echo "复制 papers/..."
        scp -r papers/ $SERVER_USER@$SERVER_IP:$SERVER_PATH/
        echo "✅ 完成！"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac
