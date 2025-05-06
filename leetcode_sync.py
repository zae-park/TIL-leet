import os
import subprocess
import json
from pathlib import Path

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRF_TOKEN = os.getenv("CSRF_TOKEN")

if not LEETCODE_SESSION or not CSRF_TOKEN:
    raise RuntimeError("LeetCode session cookie or CSRF token not provided.")

root_dir = "my_solutions"

# debug.log 초기화
with open("debug.log", "w"):
    pass

def sync_all_accepted_problems():
    temp_output = "submissions.json"
    cmd = (
        f"leetcode-export --cookies 'csrftoken={CSRF_TOKEN};LEETCODE_SESSION={LEETCODE_SESSION}' "
        f"--only-accepted --format=json --output={temp_output}"
    )
    result = os.system(cmd)
    if result != 0 or not os.path.exists(temp_output):
        raise RuntimeError("Failed to export LeetCode problems")

    with open(temp_output, "r", encoding="utf-8") as f:
        submissions = json.load(f)

    for sub in submissions:
        lang = sub["lang"]
        ext = lang_to_extension(lang)
        if not ext:
            print(f"Skipping unsupported language: {lang}")
            continue

        qid = sub.get("frontendQuestionId") or sub.get("questionFrontendId") or "unknown"
        title_slug = sub["titleSlug"]
        folder_name = f"{qid}-{title_slug}"

        dir_path = Path(root_dir) / lang / folder_name
        dir_path.mkdir(parents=True, exist_ok=True)

        with open(dir_path / "description.md", "w", encoding="utf-8") as f:
            f.write(sub.get("translatedContent") or sub.get("content") or "")

        with open(dir_path / f"solution.{ext}", "w", encoding="utf-8") as f:
            f.write(sub["code"])

        print(f"Saved: {folder_name} ({lang})")

    os.remove(temp_output)


def lang_to_extension(lang):
    mapping = {
        "python": "py",
        "python3": "py",
        "mysql": "sql",
        "cpp": "cpp",
        "java": "java",
        "c": "c",
        "javascript": "js",
        "typescript": "ts",
        "csharp": "cs",
        "go": "go",
        "ruby": "rb",
        "rust": "rs",
        "kotlin": "kt",
        "swift": "swift",
        "scala": "scala",
        "bash": "sh"
    }
    return mapping.get(lang.lower())


sync_all_accepted_problems()
