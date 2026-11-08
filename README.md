# 从反馈到交付：中文产品开发经验

中文、移动端友好的静态研究站。原创归纳 yetone 的三个反馈循环，精选 9 篇 / 7 位一手作者经验。无追踪、无分析SDK、无远程字体或后台服务。

## 本地维护（Python 3，无第三方构建依赖）

```sh
python3 scripts/build.py --validate
python3 scripts/build.py
node --check assets/app.js
python3 -m http.server 8765 --bind 0.0.0.0
```

打开 http://localhost:8765 。生成的 `index.html` 直接提交，GitHub Pages 使用 main 根目录；`.nojekyll` 禁用 Jekyll，不在云端生成内容。

### 唯一内容来源

`data/research.json`：`yetone` 原帖分层精读；`selected` 案例；`provisional` 暂缓来源；`changes` 修订记录。每案例包含稳定 `id`、来源 `url`、作者、发布时间、核验时间、阶段与标签、`verified_facts`（原文确实陈述了什么）、`our_actions`（编辑建议）、`limits`（限制）。不存放或转载长篇原文全文。

更新步骤：本地编辑此JSON → 更新 `updated_at`（显式 +08:00）、`revision` 和 `changes` → 校验与构建 → 检查差异 → 本地测试 → 普通 git commit/push。不要只改生成HTML。没有配置爬虫或虚假的自动更新：例行研究需要连接器实际读原文后，由维护者更新同一JSON。

- 商业数据为作者自述，非审计；第三方分析与作者事实分开。
- 页面显示年份不明确时保留“不确定”，不得猜补。
- 403/429 是读取限制，不代表来源删除；404需确认后标注失效或移出精选。
- 截图仅用于解读原帖；每张均可打开原尺寸查看。
- 搜索与筛选完全本地；勾选保存在浏览器 localStorage；“保存阅读清单”下载当前筛选结果，不上传数据。

## 测试

标准库结构测试：`python3 -m unittest discover -s tests`。
可选浏览器交互测试：安装 Python Playwright 与 Chromium 后，先运行本地server，再 `python3 tests/browser_test.py`。浏览器测试只创建隔离无登录上下文，不操作任何既有会话。

## 发布

仓库：https://github.com/JerichoDing/product-dev-insights

站点：https://jerichoding.github.io/product-dev-insights/

Pages 托管只接收本地生成文件，发布后请检查公网内容版本与当前提交相符；推送成功不等于部署成功。API认证由运行环境提供，严禁在代码、remote URL、日志或数据中写入令牌。
