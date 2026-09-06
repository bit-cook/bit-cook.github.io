# AgentBoot 品牌标识 · Sunrise Prompt（日出提示符）

为 [boot.ide.pub](https://boot.ide.pub)（AgentBoot — 一条命令，启动你的 AI Agent）重新设计的完整 logo 系统。

## 设计概念

日光色圆角方砖上，一道墨色终端提示符：**大于号是命令，下划线是就位的光标**。

- 呼应官网品牌锚点色 `--sun #FFD84D`（"日光"）与「一条命令，Agent 就位」的产品叙事
- 超级椭圆（n=5）砖形 + 墨色描边 + 圆头笔画，与官网按钮/卡片的圆角轮廓语言一致
- 纯 SVG 几何，可在 CSS/SVG 中完整重建（满足 DESIGN.md「品牌符号可重建」要求）
- 字标使用 Baloo 2 Bold 轮廓（OFL 授权），对应官网 rounded 显示字体的意图

## 文件清单

| 文件 | 用途 |
|---|---|
| `svg/logo-mark.svg` | 主标志（彩砖 + 墨描边），64 网格 |
| `svg/logo-mark-dark.svg` | 暗色背景版（墨绿渐变砖 + 日光符号） |
| `svg/logo-mark-mono.svg` | 单色版（currentColor，自动适配文字色） |
| `svg/logo-glyph.svg` | 裸提示符（无砖），用于水印/小空间 |
| `svg/favicon.svg` | 站点图标（16px 加粗笔画专版） |
| `svg/wordmark.svg` | 字标（轮廓已转路径，无字体依赖） |
| `svg/logo-horizontal.svg` | 横排组合（亮底） |
| `svg/logo-horizontal-dark.svg` | 横排组合（暗底） |
| `svg/logo-stack.svg` | 竖排组合 |
| `svg/banner-zh.svg` / `banner-en.svg` | README 头图 / 社交预览 1200×630 |
| `favicon.ico` | 16/32/48 多尺寸 |
| `png/` | 全尺寸 PNG（1024→16、横幅、og-image、apple-touch-icon） |
| `site-drop-in/` | 可直接替换官网 `assets/` 的成品 |
| `brand.html` | 一页式品牌规范（家族/净空/色板/禁例/应用示例） |

## 上线替换（官网）

1. `site-drop-in/favicon.svg` → 覆盖 `assets/favicon.svg`
2. `site-drop-in/apple-touch-icon.png` → 放到站点根目录
3. `site-drop-in/logo-mark.svg` → 可选：替换导航条 CSS 绘制的 `.brand-mark`
4. `<head>` 增加一行：
   `<link rel="apple-touch-icon" href="/apple-touch-icon.png">`
5. GitHub 仓库 → Settings → Social preview 上传 `png/og-image.png`
6. README 顶部加：
   ` <p align="center"><img src="banner-zh.svg" alt="AgentBoot"></p> `（或用 og-image.png）

## 色板

墨 Ink `#12251D` · 纸 Paper `#FFFDF5` · 日光 Sun `#FFD84D` · 日光深 `#FFC33A` · 行动绿 `#137A52` · 珊瑚 `#FF7A59`

## 规则速记

- 净空 = 图标高度的 1/4；最小可用 16px（favicon 用专版）
- 不拉伸、不旋转、不改配色、不加投影；单色场景用 `logo-mark-mono.svg`
- 暗底优先用 `logo-mark-dark.svg`；横排暗底用 `logo-horizontal-dark.svg`

---
生成方式：几何与排版全部脚本化（Python + HarfBuzz 塑形 + fontTools 轮廓提取），可用 `build_family.py` / `banner.py` / `brand.py` 复现与微调。
