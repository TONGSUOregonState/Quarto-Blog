from datetime import date
import subprocess

today = date.today().isoformat()
log = subprocess.getoutput('git log --since="1 day ago" --pretty=format:"- %ad %s" --date=short')
with open("updates.qmd", "w", encoding="utf-8") as f:
    f.write(f"---\ntitle: '更新日志 {today}'\n---\n\n{log}\n")
    