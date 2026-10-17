# 信创理论题库刷题网站

纯静态单文件网站（index.html，内置全部题库数据），无后端、无需构建。

## 本地预览
    python3 -m http.server 8633
浏览器打开 http://localhost:8633

## 数据更新
更新 data.json 后运行：
    python3 build_site.py
生成新的 index.html，提交推送即可自动重新部署。

## Render 部署（Static Site）
- Build Command：留空
- Static Publish Path：.（当前目录）
