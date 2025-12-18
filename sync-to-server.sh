#!/bin/bash

# 同步文件到云服务器脚本

echo "📤 同步 DSE Library 到云服务器"
echo "================================"

# 配置服务器信息（请修改这些变量）
SERVER_USER="root"                    # 你的服务器用户名
SERVER_IP="your-server-ip"            # 你的服务器 IP 地址
SERVER_PORT="22"                      # SSH 端口（默认 22）
SERVER_PATH="/var/www/dselib"         # 服务器上的目标路径

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查是否配置了服务器信息
if [ "$SERVER_IP" = "your-server-ip" ]; then
    echo -e "${RED}❌ 请先编辑脚本，配置你的服务器信息！${NC}"
    echo ""
    echo "需要修改的变量:"
    echo "  SERVER_USER - 你的服务器用户名"
    echo "  SERVER_IP - 你的服务器 IP 地址"
    echo "  SERVER_PATH - 服务器上的目标路径"
    echo ""
    echo "例如:"
    echo "  SERVER_USER=\"root\""
    echo "  SERVER_IP=\"192.168.1.100\""
    echo "  SERVER_PATH=\"/var/www/dselib\""
    exit 1
fi

echo "服务器: $SERVER_USER@$SERVER_IP:$SERVER_PATH"
echo ""

# 检查 rsync 是否安装
if ! command -v rsync &> /dev/null; then
    echo "安装 rsync..."
    sudo apt install -y rsync
fi

# 询问是否创建服务器目录
read -p "是否在服务器上创建目录? (y/n): " create_dir
if [[ $create_dir == "y" ]]; then
    echo "创建服务器目录..."
    ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "sudo mkdir -p $SERVER_PATH && sudo chown -R $SERVER_USER:$SERVER_USER $SERVER_PATH"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 目录创建成功${NC}"
    else
        echo -e "${RED}❌ 目录创建失败${NC}"
        exit 1
    fi
fi

# 同步文件
echo ""
echo -e "${YELLOW}开始同步文件...${NC}"
echo ""

# 同步前端文件（可部署部分）
echo "同步 frontend/..."
rsync -avz -e "ssh -p $SERVER_PORT" \
    --exclude='.git' \
    --exclude='papers/' \
    --exclude='admin/' \
    --exclude='archive/' \
    --exclude='*.md' \
    --exclude='*.sh' \
    --exclude='.r2-config' \
    ./frontend/ $SERVER_USER@$SERVER_IP:$SERVER_PATH/frontend/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ frontend 同步完成${NC}"
else
    echo -e "${RED}❌ frontend 同步失败${NC}"
fi

# 同步部署脚本（可选）
read -p "是否同步部署脚本和文档? (y/n): " sync_scripts
if [[ $sync_scripts == "y" ]]; then
    echo "同步脚本和文档..."
    rsync -avz -e "ssh -p $SERVER_PORT" \
        --exclude='.git' \
        --exclude='papers/' \
        --exclude='.r2-config' \
        ./ $SERVER_USER@$SERVER_IP:$SERVER_PATH/
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 脚本和文档同步完成${NC}"
    else
        echo -e "${RED}❌ 脚本同步失败${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✅ 同步完成！${NC}"
echo ""
echo "服务器路径: $SERVER_PATH"
echo ""
echo "在服务器上运行:"
echo "  cd $SERVER_PATH/frontend"
echo "  python3 -m http.server 8000"
echo ""
echo "或配置 Nginx:"
echo "  root $SERVER_PATH/frontend;"
