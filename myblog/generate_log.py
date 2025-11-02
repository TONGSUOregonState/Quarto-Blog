# generate_log.py
import os, sys, pathlib, time
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parent
SITE_ROOT = ROOT  # updates.qmd 在项目根
OUT = SITE_ROOT / "updates.qmd"

# 你想追踪的内容目录（按需增删）
WATCH_DIRS = [
    ROOT / "c-programming",
    ROOT / "matlab",
    ROOT / "c-plus-plus",
    ROOT / "Digital-Logic-Design",
    ROOT / "data-structures",
]

def iter_qmd_files():
    for d in WATCH_DIRS:
        if not d.exists():
            continue
        for p in d.rglob("*.qmd"):
            # 跳过 index.qmd / 草稿（按需）
            yield p

def rel(p: pathlib.Path):
    return p.relative_to(ROOT).as_posix()

# 收集最近更新（按修改时间降序）
files = sorted(iter_qmd_files(), key=lambda p: p.stat().st_mtime, reverse=True)

# 生成 Markdown（最简单的“最近20条”）
now = datetime.now().strftime("%Y-%m-%d %H:%M")
lines = []
lines.append("---")
lines.append('title: "更新日志"')
lines.append("freeze: false")            # 关键：每次都重新渲染
lines.append("format: html")
lines.append("---\n")
lines.append(f"*最后生成于：{now}*\n")

lines.append("## 最近更新（前 20 条）\n")
for p in files[:20]:
    mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    url = "/" + rel(p).replace(".qmd", ".html")  # 简单推 URL
    title = p.stem.replace("-", " ")
    # 如果各页面有 title 元数据，可进一步解析 YAML 获取真实标题（此处从简）
    lines.append(f"- **[{title}]({url})** — {mtime}")

new_content = "\n".join(lines) + "\n"

# 比较旧内容，避免不必要写入；但即便不写，也要 touch 一下让 mtime 变化
old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
if new_content != old:
    OUT.write_text(new_content, encoding="utf-8")
else:
    os.utime(OUT, None)  # 触发 mtime 更新，确保 Quarto 认为它变了
