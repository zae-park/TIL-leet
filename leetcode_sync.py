import os
import shutil
from pathlib import Path

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRF_TOKEN = os.getenv("CSRF_TOKEN")

if not LEETCODE_SESSION or not CSRF_TOKEN:
    raise RuntimeError("LeetCode session cookie or CSRF token not provided.")

# 원시 export 폴더
raw_dir = Path("leetcode_raw_export")
if raw_dir.exists():
    shutil.rmtree(raw_dir)
raw_dir.mkdir()

# export 실행 (언어 필터 없음)
os.system(
    f"leetcode-export --cookies 'csrftoken={CSRF_TOKEN};LEETCODE_SESSION={LEETCODE_SESSION}' "
    f"--only-accepted --folder {raw_dir}"
)

# 최종 목적지
root_dir = Path("my_solutions")

def restructure_exports():
    for problem_folder in raw_dir.iterdir():
        if not problem_folder.is_dir():
            continue

        # 메타 파일에서 id, slug 추출
        meta_file = problem_folder / "meta.json"
        if not meta_file.exists():
            print(f"Skipping {problem_folder}, no meta.json found.")
            continue

        import json
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)

        qid = meta.get("questionFrontendId", "unknown")
        slug = meta.get("titleSlug", problem_folder.name)
        lang = meta.get("lang", "unknown").lower()
        ext = lang_to_extension(lang)

        if not ext:
            print(f"Unsupported language: {lang} for {qid}-{slug}")
            continue

        new_path = root_dir / lang / f"{qid}-{slug}"
        new_path.mkdir(parents=True, exist_ok=True)

        # 파일 복사
        shutil.copy(problem_folder / "description.md", new_path / "description.md")
        shutil.copy(problem_folder / "solution.txt", new_path / f"solution.{ext}")

        print(f"Saved: {qid}-{slug} ({lang})")

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

restructure_exports()
