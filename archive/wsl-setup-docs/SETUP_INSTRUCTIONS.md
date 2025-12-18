# WSL环境迁移与Cline CLI配置 - 快速执行指南

## 第一步: 检查WSL状态 (在PowerShell中执行)

```powershell
wsl --status
wsl --list --verbose
wsl --version
```

## 第二步: 从WSL打开项目

```bash
wsl
cd /mnt/d/CODING/dselib
code .
```

## 第三步: 清理冗余文件

```bash
# 归档WSL相关文档
mkdir -p archive/wsl-setup-docs
mv WSL_*.md archive/wsl-setup-docs/
mv CELINE_CLI_INSTALL_GUIDE.md archive/wsl-setup-docs/
mv wsl_fix_403.ps1 archive/wsl-setup-docs/
mv "WSL_中断后403修复" archive/wsl-setup-docs/ 2>/dev/null
mv WS archive/wsl-setup-docs/ 2>/dev/null
```

## 第四步: 安装Cline CLI (在WSL中)

```bash
# 检查Node.js
node --version
# 如果未安装:
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装Cline
npm install -g @anthropic-ai/cline

# 验证安装
cline --version
```

## 第五步: 配置Cline

```bash
# 编辑配置文件
code .cline/config.json

# 将 YOUR_ANTHROPIC_API_KEY_HERE 替换为你的实际API密钥
# 获取API密钥: https://console.anthropic.com/
```

## 第六步: 验证配置

```bash
# 启动Cline
cline

# 或查看帮助
cline --help
```

## 第七步: 项目开发测试

```bash
# 测试Python环境
python3 --version
pip3 install -r requirements.txt

# 测试前端服务器
cd frontend
python3 -m http.server 8000
# 访问 http://localhost:8000
```

---

## 快速执行清单

- [ ] 执行WSL状态检查
- [ ] 从WSL打开项目
- [ ] 清理冗余文件
- [ ] 安装Node.js (如需要)
- [ ] 安装Cline CLI
- [ ] 配置Cline API密钥
- [ ] 验证Cline配置
- [ ] 测试Python环境
- [ ] 测试前端服务器

## 注意事项

1. 确保已启用WSL功能
2. API密钥需要从 [Anthropic Console](https://console.anthropic.com/) 获取
3. 如遇权限问题，请使用 `sudo` 权限执行安装命令
4. 前端服务器启动后可通过浏览器访问测试页面