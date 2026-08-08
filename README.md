# leeon 素材库 · 仓库页

> 数据党 leeon 的全平台可复用素材仓库，GitHub Pages 托管，浏览器直接看。

## 访问

- 仓库页（GitHub Pages）：https://l1968410560-cell.github.io/leeon-assets/
- 本地文件：`leeon/素材库网站/index.html`（双击打开）

> 提示：`index.html` 是**单文件自包含版**（SVG 内嵌、PNG 以 base64 内嵌），任何浏览器打开都无需联网读取本地资源；字体在线预览、离线时回退系统字体。

## 包含内容

| 分类 | 数量 | 来源 / 许可 |
|---|---|---|
| 通用图标 | 93 | Lucide · ISC |
| 品牌图标 | 9 | Simple Icons · CC0（logo 为各公司商标） |
| IP 形象（Q 版机器人） | 12 | DiceBear bottts · 免费商用 |
| 科技风插画 | 52 | unDraw · 免费商用免署名 |
| 字体 | 14 字重 | 思源黑体/宋体 · SIL OFL |
| 视频风格模板 | 6 | 自建模板 |
| 评论截图卡片 | 6 | 自采 |
| 品牌资产 | 品牌卡 / 色板 / 头像水印 | 自建 |

## 以后加了新素材怎么更新

1. 把新素材放进 `leeon/素材库/` 对应文件夹（沿用命名规范）。
2. 双击运行 `更新素材库网站.ps1`（或手动：`python build_site.py` 后 `git add -A && git commit && git push`）。
3. 等 1-2 分钟 GitHub Pages 自动更新，刷新网址即可看到。

## 说明

- 页面由 `build_site.py` 自动生成，素材扫描自 `素材库/` 与 `模板库/`。
- 文章原文、内部笔记不进入本仓库，只收录可复用素材。
- 许可证明细见页面底部速查表，各子目录 README 有详细说明。
