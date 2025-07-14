# Vue 项目

本项目为基于 Vue 的前端应用，支持通过 GitHub Pages (github.io) 直接访问。

## 本地开发

```bash
npm install
npm run serve
```

## 构建与部署到 GitHub Pages

1. 修改 `vue.config.js`，设置 `publicPath` 为 `/仓库名/`（请替换为你的仓库名）。
2. 构建项目：
   ```bash
   npm run build
   ```
3. 将 `dist/` 目录内容复制到 `docs/` 目录：
   ```bash
   rm -rf docs
   mkdir docs
   cp -r dist/* docs/
   ```
4. 推送到 GitHub，并在仓库 Settings → Pages 选择 `docs/` 目录作为发布源。

## 访问

访问地址：`https://你的用户名.github.io/你的仓库名/`
