# build 目录说明

## 目录作用

此目录包含项目的构建配置文件。

## 文件说明

- **constant.ts**：构建常量配置（如端口号等）
- **vite/**：Vite构建工具的插件配置
  - **plugins/**：各种Vite插件的配置文件
    - `autoImport.ts`：自动导入配置
    - `component.ts`：组件自动注册配置
    - `compress.ts`：压缩配置
    - `imagemin.ts`：图片压缩配置
    - `index.ts`：插件入口
    - `progress.ts`：构建进度条配置
    - `restart.ts`：重启配置
    - `unocss.ts`：UnoCSS配置
    - `visualizer.ts`：构建分析配置

## 注意事项

1. **配置文件**：这些文件用于配置Vite构建工具的行为
2. **修改建议**：如需修改构建配置，请谨慎修改，避免影响构建过程
3. **版本控制**：建议将此目录提交到Git，确保团队使用相同的构建配置

## 相关命令

开发环境构建：
```bash
npm run dev
```

生产环境构建：
```bash
npm run build
```

