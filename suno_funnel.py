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
