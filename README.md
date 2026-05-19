# 🎵 Suno Funnel — AI 音乐工具箱

> 专为 Suno AI / 汽水音乐创作者打造的翻唱 & Remix 提示词工具箱

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

## ⚡ 快速开始（3步）

```bash
# 1. 下载
git clone https://github.com/2569658930/tan.git
cd tan

# 2. 安装（无需额外依赖，Python 标准库即可）
# 没有 requirements.txt，开箱即用

# 3. 开始用
python3 suno_funnel.py cover 周杰伦 晴天 piano
```

## 🎯 功能

### 🎤 Cover 翻唱生成
```bash
python3 suno_funnel.py cover 陈奕迅 好久不见 acoustic
python3 suno_funnel.py cover Taylor Swift "Love Story" piano
```
自动生成 Suno 提示词 + 汽水音乐上架建议

### 🎛️ Remix 重混生成
```bash
python3 suno_funnel.py remix "夏日海滩夜晚" electronic
python3 suno_funnel.py remix "深夜城市霓虹" lofi
```
一键生成 Remix 风格的 Suno prompt

### 🔍 风格反向查询
```bash
python3 suno_funnel.py style 林俊杰
python3 suno_funnel.py style BTS
```
输入艺人名 → 输出该艺人的风格标签，直接贴进 Suno

### 📦 批量歌词处理
```bash
python3 suno_funnel.py batch my_lyrics.txt
```
把你的歌词文件批量转成 Suno 提示词

## 📋 支持的风格

### Cover 风格 (8种)
`acoustic` · `piano` · `orchestral` · `lofi` · `rock` · `electronic` · `jazz` · `chinese_traditional`

### 曲风模板 (10种)
`ballad` · `rock` · `electronic` · `r&b` · `hiphop` · `folk` · `jazz` · `lofi` · `chinese_style` · `kpop`

### 艺人风格库 (15位)
周杰伦 · 林俊杰 · 邓紫棋 · 陈奕迅 · 五月天 · 蔡依林 · 薛之谦 · 王菲 · 陶喆 · 李荣浩 · Taylor Swift · BTS · Bruno Mars · Adele · Ed Sheeran

## 🎵 适用平台

- **Suno AI** — 直接复制 prompt 生成歌曲
- **汽水音乐** — 附带上传建议（分类/标题/描述）
- **Udio** — 兼容 Udio prompt 格式

## 💡 汽水音乐 Cover 上传 Tips

| 操作 | 建议 |
|------|------|
| 分类 | 选「**原创**」而非「翻唱」 |
| 标题 | `{歌曲名} ({风格} Cover)` |
| 描述 | 标注「AI翻唱版，仅供学习交流」 |
| 平台审核重点 | **音频质量** > 版权声明 |
| 底线 | BPM 一致 + 不引用原曲片段 |

## 🤝 支持我

如果这个工具帮到了你，请：

- ⭐ **Star** 这个仓库
- 💰 **[Buy Me a Coffee](https://www.buymeacoffee.com/2569658930)**
- 💖 **[GitHub Sponsors](https://github.com/sponsors/2569658930)**
- 📢 分享给你的音乐人朋友

## 📄 License

MIT — 随便用，随便改，随便分享。

---

*Made with ❤️ for the AI music community. 一起解放音乐创作力！*
