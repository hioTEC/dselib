# DSE Library 开发说明

## 发现的问题

### 1. 数据索引混乱
- **问题**: index.json中部分中文试卷路径指向错误目录
- **示例**: `public/downloads/bafs/dse/chi/2012/ans.pdf` 应该是 `public/downloads/chi/dse/chi/2012/ans.pdf`
- **影响**: 导致PDF文件无法正确访问

### 2. 科目匹配问题
- **问题**: 前端getMeta函数使用includes匹配，可能导致误匹配
- **示例**: "Chinese" 可能匹配到其他包含"chi"的科目

### 3. 公民与社会发展数据格式
- **问题**: citizen科目的数据格式与其他科目不一致
- **观察**: 缺少某些年份的数据

## 修复计划

### 阶段1: 修复索引数据
- [ ] 重新生成index.json，确保路径正确
- [ ] 验证所有PDF文件路径的一致性

### 阶段2: 优化前端匹配逻辑
- [ ] 改进getMeta函数的匹配算法
- [ ] 添加更严格的科目名称匹配

### 阶段3: 数据验证
- [ ] 检查所有科目的数据完整性
- [ ] 验证文件路径和实际文件的一致性

## 技术细节

### 路径转换逻辑
```javascript
// 当前修复的路径转换
resolveFilePath(p) {
    if (!p) return '#';
    if (p.startsWith('public/downloads/')) {
        return '/' + p.replace('public/downloads/', 'papers/');
    }
    return p.startsWith('/') ? p : '/' + p;
}
```

### 科目元数据配置
```javascript
const SUBJECT_META = {
    'Chinese': { zh: '中文', en: 'Chinese', displayKey: 'chi', category: 'Core', icon: 'history_edu' },
    'Citizenship': { zh: '公民與社會發展', en: 'Citizenship', displayKey: 'cs', category: 'Core', icon: 'public' },
    // ... 其他科目
};
```

## 清理工作

### 已完成
- [x] 删除WSL和Cline相关配置文件
- [x] 清理admin目录中的Windows批处理文件
- [x] 移动备份文件到develop-notes
- [x] 修复PDF路径转换逻辑
- [x] 重新配置服务器从根目录启动

### 待处理
- [ ] 重新生成正确的index.json
- [ ] 验证所有PDF文件的完整性
- [ ] 优化前端科目匹配逻辑

## 测试清单

### 功能测试
- [ ] 中文科目试卷显示和下载
- [ ] 公民与社会发展科目试卷显示和下载
- [ ] 其他科目功能正常
- [ ] 路径转换正确工作
- [ ] 响应式设计在各设备正常

### 性能测试
- [ ] 首页加载速度
- [ ] 大量PDF文件的处理性能
- [ ] 移动端用户体验