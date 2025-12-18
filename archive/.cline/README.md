# Cline CLI 配置指南

本目录包含 Cline CLI 工具的配置文件，用于自定义 AI 助手的行为和项目特定设置。

## 📁 文件说明

### `config.json.template`
配置文件模板，包含所有可用的配置选项和默认值。这是一个参考文件，**请勿直接编辑**。

### `config.json`
实际使用的配置文件（此文件已被 `.gitignore` 排除，不会上传到 Git）。

## 🚀 快速开始

### 1. 创建配置文件

将模板文件复制为实际配置文件：

```bash
# Windows PowerShell
Copy-Item .cline/config.json.template .cline/config.json

# Windows CMD
copy .cline\config.json.template .cline\config.json

# Linux/macOS
cp .cline/config.json.template .cline/config.json
```

### 2. 配置 API 密钥

编辑 `config.json` 文件，填写你的 Anthropic API 密钥：

```json
{
  "apiProvider": "anthropic",
  "apiKey": "sk-ant-api03-xxxxxxxxxxxxxx",
  ...
}
```

**获取 API 密钥：**
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 登录或注册账号
3. 进入 API Keys 页面
4. 创建新的 API 密钥
5. 将密钥复制到配置文件中

### 3. 自定义配置（可选）

根据你的需求调整其他配置项（详见下方配置说明）。

## ⚙️ 配置选项详解

### API 配置

```json
{
  "apiProvider": "anthropic",     // API 提供商（目前支持 anthropic）
  "apiKey": "YOUR_API_KEY",       // 你的 API 密钥（必填）
  "model": "claude-3-5-sonnet-20241022",  // 使用的模型
  "maxTokens": 8096,              // 最大 token 数
  "temperature": 0.7              // 创造性参数（0-1，越高越有创造性）
}
```

### 项目上下文

```json
{
  "projectContext": {
    "name": "DSE Library",        // 项目名称
    "description": "...",         // 项目描述
    "type": "fullstack-web",      // 项目类型
    "language": "zh-CN",          // 项目主要语言
    "mainLanguages": [...],       // 使用的编程语言
    "frameworks": [...],          // 使用的框架
    "architecture": {...}         // 架构说明
  }
}
```

### 代码风格

```json
{
  "codeStyle": {
    "indent": 2,                  // 缩进空格数（2 或 4）
    "quotes": "single",           // 引号类型（single 或 double）
    "semicolons": false,          // 是否使用分号
    "lineWidth": 100              // 每行最大字符数
  }
}
```

### 功能开关

```json
{
  "features": {
    "autoFormat": true,           // 自动格式化代码
    "linting": true,              // 启用代码检查
    "testing": false,             // 自动运行测试
    "autoSave": true,             // 自动保存文件
    "verboseOutput": false,       // 详细输出模式
    "confirmBeforeExecute": true  // 执行命令前确认
  }
}
```

### 路径配置

```json
{
  "paths": {
    "frontend": "./frontend",     // 前端代码目录
    "admin": "./admin",           // 管理工具目录
    "papers": "./papers",         // 试卷文件目录
    "data": "./frontend/public/data"  // 数据文件目录
  }
}
```

### 偏好设置

```json
{
  "preferences": {
    "language": "zh-CN",          // 界面语言
    "timezone": "Asia/Shanghai",  // 时区
    "dateFormat": "YYYY-MM-DD",   // 日期格式
    "logLevel": "info"            // 日志级别（debug/info/warn/error）
  }
}
```

## 🔒 安全注意事项

⚠️ **重要提醒：**

1. **永远不要将 `config.json` 提交到 Git 仓库**
   - 此文件包含敏感的 API 密钥
   - 已通过 `.gitignore` 自动排除
   - 如果不小心提交，请立即撤销并重置 API 密钥

2. **不要在公共场合分享配置文件**
   - 不要在截图中暴露 API 密钥
   - 不要通过聊天工具发送完整配置文件
   - 分享时请使用 `config.json.template` 模板

3. **定期更换 API 密钥**
   - 如果怀疑密钥泄露，立即在 Anthropic Console 中撤销
   - 创建新密钥并更新配置文件

## 🔧 使用示例

### 基础配置（推荐）

适合大多数用户的基础配置：

```json
{
  "apiProvider": "anthropic",
  "apiKey": "YOUR_API_KEY_HERE",
  "model": "claude-3-5-sonnet-20241022",
  "maxTokens": 8096,
  "temperature": 0.7
}
```

### 开发模式配置

适合活跃开发阶段：

```json
{
  "apiProvider": "anthropic",
  "apiKey": "YOUR_API_KEY_HERE",
  "model": "claude-3-5-sonnet-20241022",
  "maxTokens": 8096,
  "temperature": 0.5,
  "features": {
    "autoFormat": true,
    "linting": true,
    "verboseOutput": true,
    "confirmBeforeExecute": false
  }
}
```

### 生产部署配置

适合部署和维护阶段：

```json
{
  "apiProvider": "anthropic",
  "apiKey": "YOUR_API_KEY_HERE",
  "model": "claude-3-5-sonnet-20241022",
  "maxTokens": 4096,
  "temperature": 0.3,
  "features": {
    "autoFormat": true,
    "linting": true,
    "verboseOutput": false,
    "confirmBeforeExecute": true
  }
}
```

## 📊 模型选择指南

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| `claude-3-5-sonnet-20241022` | 最新版本，性能均衡 | **推荐**：日常开发 |
| `claude-3-5-sonnet-20240620` | 稳定版本 | 需要稳定性的项目 |
| `claude-3-opus-20240229` | 最强性能，但较慢 | 复杂问题解决 |
| `claude-3-haiku-20240307` | 快速响应，成本低 | 简单任务、测试 |

## 🐛 故障排除

### 配置文件不生效

1. 检查 JSON 格式是否正确（使用 JSON 验证工具）
2. 确认文件名为 `config.json`（不是 `config.json.txt`）
3. 确认文件编码为 UTF-8

### API 密钥错误

1. 检查密钥是否完整复制（没有多余空格）
2. 确认密钥在 Anthropic Console 中仍然有效
3. 检查 API 配额是否用尽

### 命令执行失败

1. 检查路径配置是否正确
2. 确认相关目录存在
3. 检查文件权限

## 📚 相关资源

- [Anthropic API 文档](https://docs.anthropic.com/)
- [Cline CLI 官方文档](https://github.com/cline/cline)
- [DSE Library 项目文档](../README.md)

## 💡 最佳实践

1. **开发环境和生产环境使用不同的配置文件**
   - 可以创建 `config.dev.json` 和 `config.prod.json`
   - 根据需要切换

2. **定期备份配置文件**
   - 在本地安全位置保存配置副本
   - 使用密码管理器存储 API 密钥

3. **团队协作**
   - 共享 `config.json.template` 模板
   - 每个成员使用自己的 API 密钥
   - 在团队文档中说明配置差异

4. **版本控制**
   - 模板文件（`config.json.template`）应提交到 Git
   - 实际配置文件（`config.json`）不应提交
   - 在 README 中说明配置步骤

## 🔄 更新日志

### v1.0.0 (2024-12-18)
- 初始配置文件模板
- 支持 Anthropic Claude API
- 包含项目特定的 DSE Library 配置

---

**需要帮助？** 请查看项目主 README 或提交 Issue。
