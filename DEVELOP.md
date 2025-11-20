# 开发环境说明

## 📁 目录结构

### 生产环境（运行用）
```
/Users/suonian/mcp/yuque-mcpserver
```
- **用途**: 仅用于运行代理服务
- **状态**: 保持稳定，不进行开发
- **更新**: 从 GitHub 拉取稳定版本

### 开发环境
```
/Users/suonian/cursor/yuque-mcpserver
```
- **用途**: 所有开发工作在此进行
- **分支**: develop（开发分支）
- **更新**: 开发完成后推送到 GitHub，然后更新生产环境

## 🔄 工作流程

### 开发流程
1. 在开发目录进行开发
2. 提交到 develop 分支
3. 推送到 GitHub
4. 合并到 main 分支（稳定后）
5. 更新生产环境

### 更新生产环境
```bash
cd /Users/suonian/mcp/yuque-mcpserver
git pull origin main
./start_server.sh restart
```

## 📋 开发规范

- 开发分支: `develop`
- 主分支: `main`（生产环境使用）
- 提交前确保代码测试通过
- 重要更新需要更新 CHANGELOG.md

## ⚠️ 注意事项

- **不要**在生产环境直接修改代码
- **不要**在生产环境创建新分支
- 所有开发工作都在开发目录进行
