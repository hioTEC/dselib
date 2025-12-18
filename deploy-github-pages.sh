#!/bin/bash

# GitHub Pages 部署脚本 (纯 Bash 版本)

echo "🚀 开始部署 DSE Library 到 GitHub Pages..."

# 检查当前目录
if [ ! -d "frontend" ]; then
    echo "❌ 错误: frontend 目录不存在"
    exit 1
fi

# 检查是否在 Git 仓库中
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "❌ 错误: 不在 Git 仓库中"
    exit 1
fi

# 获取远程仓库信息
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "❌ 错误: 没有配置远程仓库"
    exit 1
fi

echo "📦 远程仓库: $REMOTE_URL"

# 检查是否有未提交的更改
if ! git diff --quiet; then
    echo "⚠️  警告: 有未提交的更改，建议先提交"
    echo "   运行: git add . && git commit -m '你的提交信息'"
    read -p "是否继续? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 创建 gh-pages 分支（如果不存在）
echo "🔧 创建/切换到 gh-pages 分支..."
if git show-ref --verify --quiet refs/heads/gh-pages; then
    git checkout gh-pages
else
    git checkout --orphan gh-pages
fi

# 清理当前目录（保留 .git）
echo "🧹 清理目录..."
git rm -rf . 2>/dev/null || true

# 复制 frontend 内容到根目录
echo "📋 复制 frontend 内容..."
cp -r frontend/* . 2>/dev/null

# 创建 .nojekyll 文件（禁用 Jekyll 处理）
touch .nojekyll

# 添加所有文件
echo "➕ 添加文件到 Git..."
git add .

# 检查是否有更改
if git diff --cached --quiet; then
    echo "ℹ️  没有新的更改需要部署"
    git checkout main
    exit 0
fi

# 提交
echo "📝 提交更改..."
git commit -m "Deploy to GitHub Pages - $(date '+%Y-%m-%d %H:%M:%S')"

# 推送
echo "🚀 推送到 GitHub..."
git push origin gh-pages --force

# 切换回主分支
git checkout main

echo "✅ 部署完成！"
echo "🌐 访问: https://hioTEC.github.io/dselib/"
echo "💡 提示: 如果这是第一次部署，请在 GitHub 仓库设置中启用 Pages"
echo "   1. 进入 Settings > Pages"
echo "   2. 选择 gh-pages 分支作为源"
echo "   3. 保存并等待几分钟"
