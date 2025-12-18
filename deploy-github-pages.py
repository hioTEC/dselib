#!/usr/bin/env python3
"""
GitHub Pages 部署脚本
将 frontend 目录推送到 GitHub Pages
"""

import os
import subprocess
import sys

def run_cmd(cmd, check=True):
    """运行命令并返回结果"""
    print(f"🔧 执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ 错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    print("🚀 开始部署 DSE Library 到 GitHub Pages...")
    
    # 检查当前目录
    if not os.path.exists("frontend"):
        print("❌ 错误: frontend 目录不存在")
        sys.exit(1)
    
    # 检查是否在 Git 仓库中
    result = run_cmd("git rev-parse --is-inside-work-tree", check=False)
    if result.returncode != 0:
        print("❌ 错误: 不在 Git 仓库中")
        sys.exit(1)
    
    # 获取远程仓库信息
    remote_result = run_cmd("git remote get-url origin", check=False)
    if remote_result.returncode != 0:
        print("❌ 错误: 没有配置远程仓库")
        sys.exit(1)
    
    remote_url = remote_result.stdout.strip()
    print(f"📦 远程仓库: {remote_url}")
    
    # 创建 gh-pages 分支（如果不存在）
    print("🔧 创建 gh-pages 分支...")
    run_cmd("git checkout --orphan gh-pages 2>/dev/null || git checkout gh-pages")
    
    # 清理当前目录（保留 .git）
    print("🧹 清理目录...")
    run_cmd("git rm -rf . 2>/dev/null || true")
    
    # 复制 frontend 内容到根目录
    print("📋 复制 frontend 内容...")
    run_cmd("cp -r frontend/* .")
    
    # 创建 .nojekyll 文件（禁用 Jekyll 处理）
    run_cmd("touch .nojekyll")
    
    # 添加所有文件
    print("➕ 添加文件到 Git...")
    run_cmd("git add .")
    
    # 提交
    print("📝 提交更改...")
    run_cmd('git commit -m "Deploy to GitHub Pages"')
    
    # 推送
    print("🚀 推送到 GitHub...")
    run_cmd("git push origin gh-pages --force")
    
    print("✅ 部署完成！")
    print("🌐 访问: https://hioTEC.github.io/dselib/")
    print("💡 提示: 在 GitHub 仓库设置中启用 Pages，选择 gh-pages 分支")

if __name__ == "__main__":
    main()
