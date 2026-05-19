#!/usr/bin/env python3
"""
🎵 Suno Funnel — AI 音乐翻唱/Cover 提示词工具箱

用法:
  python3 suno_funnel.py cover  原唱 原曲名 → 生成 Cover 提示词
  python3 suno_funnel.py remix  歌曲描述    → 生成 Remix 提示词  
  python3 suno_funnel.py style  参考艺人    → 反向生成风格提示词
  python3 suno_funnel.py batch  lyrics.txt  → 批量歌词转提示词
"""

import argparse
import json
import sys
from pathlib import Path

# ── 风格数据库 ──────────────────────────────────────────────────────
STYLE_DB = {
    "周杰伦": "Mandarin pop, R&B, piano ballad, Chinese style pentatonic, melancholic male vocal, 80-100 BPM",
    "林俊杰": "Mandarin pop ballad, powerful tenor vocal, piano-driven, emotional, wide vocal range, 70-90 BPM",
    "邓紫棋": "Mandarin pop, powerful female vocal, rock influence, high notes, emotional build-up, 80-100 BPM",
    "陈奕迅": "Cantopop ballad, deep baritone vocal, minimalist arrangement, storytelling, 60-80 BPM",
    "五月天": "Mandarin rock, band sound, uplifting, guitar-driven, stadium anthem, 120-140 BPM",
    "蔡依林": "Mandopop dance, electronic, female vocal, upbeat, synth-heavy, 120-130 BPM",
    "薛之谦": "Mandarin ballad, emotional male vocal, string arrangement, dramatic, 70-85 BPM",
    "王菲": "Art pop, ethereal female vocal, dreamy, reverb-heavy, atmospheric, 60-80 BPM",
    "陶喆": "Mandarin R&B, soulful male vocal, falsetto, groovy bass, 80-100 BPM",
    "李荣浩": "Mandarin pop, laid-back male vocal, guitar-based, minimalist production, 70-90 BPM",
    "Taylor Swift": "Pop, confessional female vocal, acoustic guitar, storytelling, 80-120 BPM",
    "BTS": "K-pop, rap, vocal harmony, electronic, dance, 120-140 BPM",
    "Bruno Mars": "Funk, soul, retro pop, male vocal, groovy bass, 100-115 BPM",
    "Adele": "Soul pop, powerful female vocal, piano, emotional ballad, 60-80 BPM",
    "Ed Sheeran": "Pop folk, acoustic guitar, male vocal, loop pedal, 80-100 BPM",
}

GENRE_TEMPLATES = {
    "ballad": "slow tempo, emotional piano, string orchestra, heartfelt vocal, reverb, cinematic",
    "rock": "electric guitar, drums, bass, energetic, distorted, 120-140 BPM, stadium sound",
    "electronic": "synth, arpeggiator, 808 drums, sidechain compression, 120-130 BPM, club energy",
    "r&b": "smooth, groovy bass, soulful vocal, 808 kick, chill vibe, 80-100 BPM",
    "hiphop": "trap beat, 808 bass, hi-hat rolls, rap vocal, urban, 140-160 BPM",
    "folk": "acoustic guitar, warm vocal, simple arrangement, storytelling, 70-90 BPM",
    "jazz": "swing, piano trio, walking bass, brush drums, improvised feel, 100-120 BPM",
    "lofi": "chillhop, vinyl crackle, mellow, study beats, filtered drums, 70-90 BPM",
    "chinese_style": "古风, 中国五声调式, 笛子, 古筝, 琵琶, 二胡, 悠远, 60-80 BPM",
    "kpop": "polished production, vocal layering, dance beat, catchy hook, 110-130 BPM",
}

COVER_TEMPLATES = {
    "acoustic": "acoustic cover, stripped down, soft guitar, intimate vocal, raw emotion",
    "piano": "piano cover, solo piano arrangement, classical influence, minimal, spacious",
    "orchestral": "orchestral cover, cinematic strings, epic, film score style, dramatic build",
    "lofi": "lofi cover, chill beats, warm vinyl sound, relaxed version, bedroom pop",
    "rock": "rock cover, electric guitar reinterpretation, band energy, powerful drums",
    "electronic": "electronic cover, synth remake, retro 80s, vaporwave, digital reimagining",
    "jazz": "jazz cover, swing reinterpretation, walking bass, lounge piano, sophisticated",
    "chinese_traditional": "国风改编, 民乐版, 古筝和笛子主导, 戏曲元素, 悠远意境",
}


def generate_cover(original_artist: str, song_title: str, cover_style: str = "piano") -> str:
    """生成翻唱提示词"""
    style_prompt = COVER_TEMPLATES.get(cover_style, COVER_TEMPLATES["piano"])
    
    prompt = f"""[Cover Version]
Original: {original_artist} - {song_title}
Style: {cover_style.title()} Cover

🎤 **Suno Prompt:**
A {style_prompt}, cover of {song_title} originally by {original_artist}, reimagined with emotional depth and fresh interpretation. High quality production, clear vocals, warm mix.

📝 **Style Tags:** {style_prompt}

💡 **Tips:**
- 上传到汽水音乐选「原创」分类
- 标题格式: {song_title} ({cover_style} Cover)
- 描述写: AI翻唱版，仅供学习交流
"""
    return prompt


def generate_remix(description: str, genre: str = "electronic") -> str:
    """生成 Remix 提示词"""
    genre_prompt = GENRE_TEMPLATES.get(genre, GENRE_TEMPLATES["electronic"])
    
    prompt = f"""[Remix Version]
Theme: {description}
Style: {genre.title()} Remix

🎤 **Suno Prompt:**
A {genre_prompt} remix, {description}. Driving energy, powerful drop, professional production, club-ready sound, clean mastering.

📝 **Style Tags:** {genre_prompt}

💡 **Tips:**
- 汽水音乐上传走「音频投稿」
- 标题格式: {description[:30]} ({genre} Remix)
- 过审关键: BPM一致 + 无原曲引用
"""
    return prompt


def reverse_style(artist_name: str) -> str:
    """反向查艺人风格"""
    if artist_name in STYLE_DB:
        return f"🎤 **{artist_name}** 风格:\n{STYLE_DB[artist_name]}"
    
    # Fuzzy match
    for name, style in STYLE_DB.items():
        if artist_name in name or name in artist_name:
            return f"🎤 **{name}** (匹配) 风格:\n{style}"
    
    return f"未找到 {artist_name}，试试: {', '.join(list(STYLE_DB.keys())[:10])}..."


def batch_lyrics(filepath: str) -> str:
    """批量处理歌词文件 → 生成 Suno 提示词"""
    path = Path(filepath)
    if not path.exists():
        return f"文件不存在: {filepath}"
    
    content = path.read_text(encoding='utf-8')
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    
    # 简单分割：空行分隔不同歌曲
    songs = []
    current = []
    for line in lines:
        if line == '---' or line == '===':
            if current:
                songs.append(current)
                current = []
        else:
            current.append(line)
    if current:
        songs.append(current)
    
    if not songs:
        songs = [lines]  # 整篇当作一首
    
    output = []
    for i, song_lines in enumerate(songs):
        # 取前4句作为风格参考
        sample = '\n'.join(song_lines[:4])
        first_line = song_lines[0][:30] if song_lines else "Untitled"
        
        output.append(f"""## Song {i+1}: {first_line}...

🎤 **Suno Prompt:**
Mandarin pop, emotional, storytelling, male/female vocal, clear articulation.
Lyrics theme: {sample[:100]}

📝 **Full Lyrics:**
{chr(10).join(song_lines)}
""")
    
    return '\n---\n'.join(output)


def generate_full(artist: str, theme: str, style: str = "mandarin_pop") -> str:
    """生成完整 Suno 提示词（含建议歌词结构）"""
    # 获取艺人风格
    if artist in STYLE_DB:
        artist_style = STYLE_DB[artist]
    else:
        for name, s in STYLE_DB.items():
            if artist in name or name in artist:
                artist_style = s
                artist = name
                break
        else:
            artist_style = "Mandarin pop, emotional vocal, modern production"

    # 生成歌词结构建议
    structures = {
        "standard": "Verse → Pre-Chorus → Chorus → Verse2 → Chorus → Bridge → Chorus → Outro",
        "ballad": "Verse → Verse2 → Chorus → Bridge → Chorus → Outro (slow fade)",
        "hiphop": "Intro → Verse → Hook → Verse2 → Hook → Bridge → Hook → Outro",
        "electronic": "Intro → Build → Drop → Verse → Build → Drop → Bridge → Final Drop",
    }
    structure = structures.get(style, structures["standard"])

    # 生成音色建议
    timbre_map = {
        "周杰伦": "slightly nasal, melancholic male tenor, relaxed delivery",
        "林俊杰": "powerful clear tenor, effortless high notes, emotional vibrato",
        "邓紫棋": "strong belting female vocal, gritty texture, wide dynamic range",
        "陈奕迅": "deep warm baritone, storytelling tone, understated power",
        "五月天": "band vocal, energetic rock tenor, crowd-feel",
        "蔡依林": "bright pop female vocal, precise articulation, dance energy",
        "薛之谦": "raspy emotional male, intimate delivery, whispered sections",
        "王菲": "ethereal soprano, breathy delivery, floating tone",
        "陶喆": "smooth R&B tenor, effortless falsetto, groovy phrasing",
        "李荣浩": "laid-back male vocal, conversational tone, subtle emotion",
    }
    timbre = timbre_map.get(artist, "emotional vocal, clear articulation")

    # 汽水音乐元数据
    tags_list = [t.strip() for t in artist_style.split(",")]
    genre_tags = " ".join(f"#{t.strip().replace(' ', '')}" for t in tags_list[:5])

    prompt = f"""╔══════════════════════════════════════════════════════╗
║          🎵 Suno Funnel — 完整创作模板                ║
╚══════════════════════════════════════════════════════╝

📋 **项目信息**
  艺人参考: {artist}
  创作主题: {theme}
  风格:      {style.replace('_', ' ').title()}

🎤 **Suno Prompt (直接复制贴入 Suno)**
────────────────────────────────────────────
{artist_style}. A song about {theme}, {timbre}. 
Professional production, clean mix, emotional delivery.
────────────────────────────────────────────

🎼 **建议结构**
  {structure}

🎛️ **音色设定**
  {timbre}

📝 **建议歌词模板 (填入你的歌词)**
```
[Verse 1]
({theme} — 第一段，建立场景/情绪)
...

[Pre-Chorus]
(过渡段，情绪渐进)
...

[Chorus]
(副歌，核心旋律 + 主题句)
...

[Verse 2]
(第二段，发展故事)
...

[Chorus]
(重复副歌)
...

[Bridge]
(桥段，情绪转折)
...

[Outro]
(收尾)
```

📊 **Suno 参数建议**
  时长:     3:00-4:30
  结构:     {structure}
  BPM:      {_guess_bpm(artist_style)}

🚀 **汽水音乐上传 Checklist**
  □ 分类选「原创」(不是翻唱)
  □ 标题: {theme} ({style.replace('_', ' ').title()})
  □ 标签: {genre_tags}
  □ 描述: AI音乐创作 / {artist}风格 / {theme}
  □ 音频质量检查: 无杂音、无断音、响度正常
  □ 封面: 建议 800x800 方形图

💡 **过审加分项**
  • 音频时长 > 2分钟
  • 有完整的 verse-chorus 结构
  • 歌词无敏感词
  • 标题不含原曲名 (纯原创/cover声明)
"""
    return prompt


def _guess_bpm(style_str: str) -> str:
    """从风格字符串中提取 BPM 范围"""
    import re
    match = re.search(r'(\d+-\d+) BPM', style_str)
    if match:
        return match.group(1)
    # 默认常见值
    if any(w in style_str.lower() for w in ['ballad', 'slow', 'chill']):
        return "70-90"
    elif any(w in style_str.lower() for w in ['dance', 'rock', 'energy']):
        return "120-140"
    elif any(w in style_str.lower() for w in ['hiphop', 'rap', 'trap']):
        return "140-160"
    return "90-120"


def generate_random() -> str:
    """随机生成一个创作灵感组合"""
    import random
    artist = random.choice(list(STYLE_DB.keys()))
    themes = [
        "深夜城市霓虹", "夏日海滩的告别", "雨天下的便利店",
        "地铁最后一班车", "旧照片里的笑脸", "无人接听的电话",
        "天台上的星空", "凌晨三点的便利店", "那年冬天的约定",
        "一个人的电影院", "日记本最后一页", "城市的天际线",
        "放学后的操场", "咖啡馆的窗边", "海边的烟花"
    ]
    theme = random.choice(themes)
    styles = list(COVER_TEMPLATES.keys()) + list(GENRE_TEMPLATES.keys())
    style = random.choice(styles)
    
    return generate_full(artist, theme, style)


def main():
    parser = argparse.ArgumentParser(
        description='Suno Funnel — AI 音乐翻唱/Remix 提示词工具箱',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  suno_funnel.py cover 周杰伦 晴天 piano      → 生成 Cover 提示词
  suno_funnel.py remix "夏日海滩" electronic  → 生成 Remix 提示词
  suno_funnel.py style 林俊杰                 → 查艺人风格
  suno_funnel.py batch my_lyrics.txt          → 批量转提示词
  suno_funnel.py list-styles                  → 列出所有风格模板
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # cover
    cover_parser = subparsers.add_parser('cover', help='生成 Cover 翻唱提示词')
    cover_parser.add_argument('artist', help='原唱艺人')
    cover_parser.add_argument('song', help='歌曲名')
    cover_parser.add_argument('style', nargs='?', default='piano',
                              choices=list(COVER_TEMPLATES.keys()),
                              help='翻唱风格')
    
    # remix
    remix_parser = subparsers.add_parser('remix', help='生成 Remix 提示词')
    remix_parser.add_argument('description', help='歌曲描述/主题')
    remix_parser.add_argument('genre', nargs='?', default='electronic',
                              choices=list(GENRE_TEMPLATES.keys()),
                              help='曲风')
    
    # style
    style_parser = subparsers.add_parser('style', help='反向查艺人风格标签')
    style_parser.add_argument('artist', help='艺人名')
    
    # batch
    batch_parser = subparsers.add_parser('batch', help='批量歌词 → 提示词')
    batch_parser.add_argument('filepath', help='歌词文件路径')
    
    # full — 完整 Suno 创作模板
    full_parser = subparsers.add_parser('full', help='生成完整 Suno 创作模板(含歌词结构/音色/BPM/上传清单)')
    full_parser.add_argument('artist', help='参考艺人风格')
    full_parser.add_argument('theme', help='创作主题/歌名')
    full_parser.add_argument('style', nargs='?', default='ballad',
                             choices=['ballad','rock','electronic','hiphop','standard'],
                             help='歌曲风格')

    # random — 随机灵感
    subparsers.add_parser('random', help='随机生成一个创作灵感')
    
    # list
    subparsers.add_parser('list-styles', help='列出所有风格')
    subparsers.add_parser('list-genres', help='列出所有曲风')
    
    args = parser.parse_args()
    
    if args.command == 'cover':
        print(generate_cover(args.artist, args.song, args.style))
    elif args.command == 'remix':
        print(generate_remix(args.description, args.genre))
    elif args.command == 'style':
        print(reverse_style(args.artist))
    elif args.command == 'batch':
        print(batch_lyrics(args.filepath))
    elif args.command == 'full':
        print(generate_full(args.artist, args.theme, args.style))
    elif args.command == 'random':
        print(generate_random())
    elif args.command == 'list-styles':
        print("🎤 **Cover 风格模板:**")
        for k, v in COVER_TEMPLATES.items():
            print(f"  {k:20} | {v}")
    elif args.command == 'list-genres':
        print("🎵 **曲风模板:**")
        for k, v in GENRE_TEMPLATES.items():
            print(f"  {k:20} | {v}")
    elif args.command == 'list-artists':
        print("🎤 **已收录艺人风格:**")
        for k, v in STYLE_DB.items():
            print(f"  {k:10} | {v}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
