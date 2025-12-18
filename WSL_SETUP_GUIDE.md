# WSL 开发环境设置指南

## 当前状况
WSL安装需要管理员权限，当前权限不足。

## 安装前准备

### 1. 以管理员权限运行PowerShell
- 右键点击PowerShell图标
- 选择"以管理员身份运行"
- 或按`Win + X`，选择"Windows PowerShell（管理员）"

### 2. 启用WSL功能
```powershell
# 启用WSL功能
dism /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 启用虚拟机平台
dism /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

### 3. 重启计算机
重启后继续下一步。

### 4. 设置WSL 2为默认版本
```powershell
wsl --set-default-version 2
```

### 5. 安装Linux发行版
```powershell
# 查看可用的发行版
wsl --list --online

# 安装Ubuntu (推荐)
wsl --install -d Ubuntu-22.04

# 或直接安装最新Ubuntu
wsl --install Ubuntu
```

## WSL安装步骤

### 方法1: 使用WSL安装命令 (推荐)
```powershell
# 以管理员身份运行此命令
wsl --install

# 如果需要指定发行版
wsl --install -d Ubuntu-22.04
```

### 方法2: 手动下载安装
1. 访问 Microsoft Store
2. 搜索"Linux"
3. 选择Ubuntu并安装
4. 启动Ubuntu进行初始设置

## WSL环境配置

### 1. 首次启动设置
```bash
# 启动WSL
wsl

# 创建用户名和密码
# 按照提示输入用户名和密码
```

### 2. 更新系统
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. 安装开发工具
```bash
# 安装基础开发工具
sudo apt install -y build-essential git curl wget vim

# 安装Node.js和npm
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装Python和pip
sudo apt install -y python3 python3-pip

# 安装Docker (可选)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

## 挂载Windows工作目录

### 1. 访问Windows文件
```bash
# 在WSL中访问Windows文件
ls /mnt/c/Users/$USER/

# 挂载点说明：
# /mnt/c/ -> C:\
# /mnt/d/ -> D:\
# 等等
```

### 2. 切换到工作目录
```bash
# 假设你的工作目录在D:\CODING\dselib
cd /mnt/d/CODING/dselib

# 或者在Windows路径中直接访问
cd /mnt/c/Users/PJoni/Desktop/project
```

### 3. 创建符号链接 (推荐)
```bash
# 在WSL home目录创建符号链接
ln -s /mnt/d/CODING/dselib ~/dselib

# 现在可以直接访问
cd ~/dselib
```

## 开发环境设置

### 1. Git配置
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 设置默认编辑器
git config --global core.editor vim
```

### 2. 安装Cline CLI (在WSL中)
```bash
# 在WSL中安装Cline CLI (现在应该可以工作了)
npm install -g cline

# 或使用npx (推荐)
npx cline
```

### 3. VS Code集成
```bash
# 安装VS Code WSL扩展
# 然后在WSL中：
code .

# 这将在VS Code中打开当前目录，并自动配置WSL环境
```

## 常用WSL命令

### 基本操作
```bash
# 列出所有发行版
wsl --list --verbose

# 启动特定发行版
wsl -d Ubuntu-22.04

# 关闭WSL
wsl --shutdown

# 注销发行版
wsl --unregister Ubuntu-22.04
```

### 文件操作
```bash
# 在WSL中打开Windows Explorer
explorer.exe .

# 从WSL打开Windows应用
notepad.exe filename.txt
calc.exe
```

### 网络和端口
```bash
# 查看网络配置
ip addr show

# 如果需要访问WSL中的服务
# 在Windows中访问: http://localhost:端口号
# 或使用WSL IP地址
```

## 故障排除

### 常见问题
1. **权限错误**: 确保以管理员身份运行安装命令
2. **WSL无法启动**: 检查Hyper-V是否启用
3. **网络问题**: 配置防火墙设置

### 检查系统要求
```powershell
# 检查Windows版本
winver

# 检查系统架构
wmic os get osarchitecture
```

### 重新安装WSL
```powershell
# 完全重置WSL
wsl --shutdown
wsl --unregister Ubuntu-22.04
wsl --install Ubuntu-22.04
```

## 与现有项目的集成

### 1. 克隆Git仓库
```bash
# 假设仓库在GitHub
git clone https://github.com/hioTEC/dselib.git
cd dselib
```

### 2. 设置开发环境
```bash
# 根据项目需求安装依赖
# Python项目
pip3 install -r requirements.txt

# Node.js项目
npm install

# Docker项目
docker-compose up -d
```

### 3. 启动开发服务器
```bash
# 根据项目类型启动
python3 app.py          # Python Flask/Django
npm start              # Node.js项目
python -m http.server  # 简单HTTP服务器
```

## 最佳实践

### 1. 路径处理
- 在WSL中使用Unix风格路径 (`/mnt/c/...`)
- 避免在路径中使用空格和特殊字符
- 使用符号链接简化访问

### 2. 文件权限
- 确保WSL中的文件有正确的权限
- 使用 `chmod` 调整文件权限

### 3. 环境变量
- 在 `.bashrc` 或 `.zshrc` 中设置环境变量
- 避免在Windows和WSL之间重复设置

### 4. 版本控制
- 在WSL中使用Git
- 避免在Windows和WSL中同时操作同一个Git仓库

## 总结
按照以上步骤安装和配置WSL后，你将拥有一个功能完整的Linux开发环境，可以无缝访问Windows文件系统，并支持Cline CLI等工具。
