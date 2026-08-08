# 字体素材库

> 中英文可商用字体 + 组合规范。**系统里已装得意黑、JetBrains Mono；本目录补思源黑体/宋体全字重。**

## 已收录字体

| 字体 | 文件 | 用途 | 许可 |
|---|---|---|---|
| 思源黑体 SourceHanSansCN | 7 字重（ExtraLight~Heavy） | 正文 / 标题（科技感） | [SIL OFL 1.1](https://github.com/adobe-fonts/source-han-sans)，免费商用 |
| 思源宋体 SourceHanSerifCN | 7 字重（ExtraLight~Heavy） | 编辑杂志风标题 / 引言 | [SIL OFL 1.1](https://github.com/adobe-fonts/source-han-serif)，免费商用 |
| 得意黑 SmileySans | 系统已装 | 标题 / 大数字（首选） | OFL，免费商用 |
| JetBrains Mono | 系统已装 | 数据 / 代码 / 英文数字 | OFL，免费商用 |

## 组合规范（与 `模板库/高级感升级规范.md` 一致）

- **标题 / 大数字**：得意黑（默认）→ 思源宋体 900（编辑杂志风）→ 思源黑体 Heavy（备用）
- **数据 / 英文数字**：JetBrains Mono ExtraBold
- **正文**：思源黑体 Light / Regular（避免系统默认字体）
- **引用 / 文艺段落**：思源宋体 Light / Regular
- 字号层级：大标题 72-96px，数据 100-140px，说明 14-16px，中间不留档
- 禁止：系统默认字体、圆体/幼圆正文、带衬线宋体正文

## 安装方式

将 `.otf` 文件右键 → 安装（Windows），或放入 `C:\Windows\Fonts`。PPT/视频工程若需跨设备，直接把对应 `.otf` 复制进工程 `fonts/` 目录。

## 可补充

- 得意黑：`github.com/atelier-anchor/smiley-sans`（已装，如需打包到工程可下载）
- JetBrains Mono：`github.com/JetBrains/JetBrainsMono`（已装）
- 英文艺术字体（手写/涂鸦，仅用于"手绘白板"模板注释）
