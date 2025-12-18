# Cline CLI 安装指南

## 当前状况
当前Cline CLI在Windows系统上的支持有限，大多数npm包只支持macOS和Linux系统。

## 问题分析
1. **主包cline**: 仅支持macOS和Linux
2. **离线版本cline-offline**: 仅支持macOS和Linux  
3. **Windows版本@involvex/cline-cli-win**: 安装超时或失败

## 替代解决方案

### 方案1: 使用WSL (推荐)
在Windows上使用WSL (Windows Subsystem for Linux) 来运行Cline CLI:

```bash
# 安装WSL (如果尚未安装)
wsl --install

# 进入Linux环境
wsl

# 安装Node.js和npm (如果尚未安装)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# 在Linux环境中安装Cline CLI
npm install -g cline

# 验证安装
cline --version
```

### 方案2: 使用npx运行Cline
无需全局安装，直接使用npx运行:

```bash
# 直接运行Cline
npx cline

# 或者运行最新版本
npx @cline/cli@latest
```

### 方案3: GitHub源码安装
从GitHub直接下载和安装:

```bash
# 克隆Cline仓库
git clone https://github.com/saoudrizwan/cline.git
cd cline

# 安装依赖
npm install

# 全局链接
npm link

# 运行
cline
```

### 方案4: 使用VS Code扩展
Cline主要作为VS Code扩展提供:
1. 在VS Code中搜索"Cline"
2. 安装官方Cline扩展
3. 配置API密钥后即可使用

## MCP (Model Context Protocol) 功能

Cline的核心价值在于MCP支持。如果你需要MCP功能，可以考虑:

### 安装MCP服务器
```bash
# 安装通用MCP服务器
npm install -g @modelcontextprotocol/cli

# 或安装特定用途的MCP服务器
npm install -g mcp-server-git
npm install -g mcp-server-filesystem
```

### MCP客户端工具
```bash
# 安装MCP客户端
npm install -g mcp-client
```

## 配置建议

### 环境变量配置
```bash
# 设置API密钥 (可选)
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
```

### 配置文件
Cline会在以下位置创建配置:
- Windows: `%APPDATA%/cline/`
- 或通过VS Code设置

## 使用示例

### 基本命令
```bash
# 查看帮助
cline --help

# 启动交互模式
cline

# 指定项目目录
cline --project /path/to/project

# 启用详细输出
cline --verbose
```

### 与项目集成
```bash
# 在项目目录中运行
cd your-project
cline init  # 初始化Cline配置
cline      # 开始使用
```

## 故障排除

### 常见问题
1. **权限错误**: 使用`--force`或管理员权限
2. **网络问题**: 使用代理或离线模式
3. **版本冲突**: 使用npx避免版本问题

### 调试模式
```bash
# 启用详细日志
cline --debug --verbose
```

## 替代工具
如果Cline CLI不可用，考虑这些替代方案:
- **Claude CLI**: Anthropic官方命令行工具
- **Continue**: 另一个AI编程助手
- **GitHub Copilot CLI**: GitHub的CLI工具

## 总结
虽然Cline CLI在Windows上的原生支持有限，但通过WSL、npx或源码安装等方式，仍然可以使用其核心功能。建议优先尝试WSL方案以获得最佳体验。
