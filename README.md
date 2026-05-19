# 🎵 Suno Funnel — AI 音乐工具箱

> 专为 Suno AI / 汽水音乐创作者打造的翻唱 & Remix 提示词工具箱  
> Zero-dependency, 开箱即用 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

---

## ⚡ 快速开始

```bash
git clone https://github.com/2569658930/tan.git
cd tan
python3 suno_funnel.py cover 周杰伦 晴天 piano
```

**无需安装任何依赖，Python 标准库即可运行。**

---

## 🎯 6 个命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `cover` | 翻唱提示词 | `suno_funnel.py cover 周杰伦 晴天 piano` |
| `remix` | Remix 提示词 | `suno_funnel.py remix "深夜城市霓虹" lofi` |
| `full` | 🔥 完整创作模板 | `suno_funnel.py full 周杰伦 "雨天下的便利店" ballad` |
| `random` | 🎲 随机灵感 | `suno_funnel.py random` |
| `style` | 查艺人风格 | `suno_funnel.py style 林俊杰` |
| `batch` | 批量歌词处理 | `suno_funnel.py batch my_lyrics.txt` |

### 🔥 `full` 命令 — 一站式输出

```
suno_funnel.py full 周杰伦 "雨天下的便利店" ballad
```

输出包含：
- ✅ 可直接贴入 Suno 的英文 prompt
- ✅ 完整的歌词结构模板 (Verse/Chorus/Bridge/Outro)
- ✅ 参考音色设定
- ✅ BPM 范围建议
- ✅ 汽水音乐上传 Checklist

---

## 📚 文档

| 文件 | 内容 |
|------|------|
| [TUTORIAL.md](TUTORIAL.md) | 🔥 汽水音乐 Cover 过审全攻略（实测版） |
| [PROMO.md](PROMO.md) | 推广文案（B站/抖音/微信群 三版本） |

---

## 📋 数据规模

| 类型 | 数量 | 列表 |
|------|------|------|
| Cover 风格 | 8 | `acoustic` `piano` `orchestral` `lofi` `rock` `electronic` `jazz` `chinese_traditional` |
| 曲风模板 | 10 | `ballad` `rock` `electronic` `r&b` `hiphop` `folk` `jazz` `lofi` `chinese_style` `kpop` |
| 艺人风格库 | 15 | 周杰伦 林俊杰 邓紫棋 陈奕迅 五月天 蔡依林 薛之谦 王菲 陶喆 李荣浩 Taylor Swift BTS Bruno Mars Adele Ed Sheeran |
| 灵感主题 | 15 | 深夜城市霓虹 天台上的星空 夏日海滩告别... |

---

## 🚀 汽水音乐过审速查

```
✓ 分类选「原创」
✓ 标题: {主题} ({风格})
✓ 描述: AI音乐创作实验作品
✓ BPM 对齐参考值
✓ 音频 > 1:30
✗ 别写原曲名/原唱名
✗ 别用原曲封面
✗ 别选「翻唱」分类
```

详见 [TUTORIAL.md](TUTORIAL.md)

---

## 🤝 支持我

如果这个工具帮你省了时间：

- ⭐ **Star** 这个仓库
- 💰 **[Buy Me a Coffee](https://www.buymeacoffee.com/2569658930)**
- 💖 **[GitHub Sponsors](https://github.com/sponsors/2569658930)**
- 📢 转发给做 AI 音乐的朋友

---

*Made with ❤️ for the AI music community. 一起解放音乐创作力！*
