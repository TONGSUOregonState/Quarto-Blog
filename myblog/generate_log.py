from __future__ import annotations

import pathlib
from datetime import datetime


ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "updates.qmd"


WATCH_DIRS = [
    ROOT / "c-programming",
    ROOT / "matlab",
    ROOT / "c-plus-plus",
    ROOT / "Digital-Logic-Design",
    ROOT / "data-structures",
    ROOT / "physics",
    ROOT / "mathematics",
]


def iter_qmd_files():
    for d in WATCH_DIRS:
        if not d.exists():
            continue
        yield from d.rglob("*.qmd")


def rel_path(p: pathlib.Path) -> str:
    return p.relative_to(ROOT).as_posix()


def main() -> None:
    files = sorted(iter_qmd_files(), key=lambda p: p.stat().st_mtime, reverse=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = []
    lines.append("---")
    lines.append("title: \"更新日志\"")
    lines.append("freeze: false")
    lines.append("format: html")
    lines.append("---\n")
    lines.append(f"*最后生成于: {now}*\n")

    lines.append("## 最近更新\n")
    for p in files:
        mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        url = "/" + rel_path(p).replace(".qmd", ".html")
        title = p.stem.replace("-", " ")
        lines.append(f"- **[{title}]({url})** — {mtime}")

    content = "\n".join(lines) + "\n"
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if content != old:
        OUT.write_text(content, encoding="utf-8")
    else:
        OUT.touch()


if __name__ == "__main__":
    main()

