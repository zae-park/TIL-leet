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

        # 기본 값 초기화
        qid, slug, lang = None, None, None

        # 1. 폴더명에서 id-slug 추출
        folder_parts = problem_folder.name.split("-", 1)
        if len(folder_parts) == 2:
            qid, slug = folder_parts
        else:
            slug = problem_folder.name
            qid = "unknown"

        # 2. 언어 추론
        # solution.txt 하나만 존재하므로 확장자로 판단
        ext = None
        for file in problem_folder.iterdir():
            if file.name.startswith("solution"):
                ext = guess_extension(file.suffix)
                break

        if not ext:
            print(f"Skipping {problem_folder}, 확장자 추론 실패.")
            continue

        lang = extension_to_language(ext)
        if not lang:
            print(f"Unsupported language extension: {ext}")
            continue

        new_path = root_dir / lang / f"{qid}-{slug}"
        new_path.mkdir(parents=True, exist_ok=True)

        # 파일 복사
        if (problem_folder / "description.md").exists():
            shutil.copy(problem_folder / "description.md", new_path / "description.md")
        else:
            print(f"Warning: description.md 없음 → {qid}-{slug}")

        shutil.copy(problem_folder / "solution.txt", new_path / f"solution.{ext}")
        print(f"Saved: {qid}-{slug} ({lang})")

def guess_extension(suffix):
    return suffix.lstrip(".").lower()

def extension_to_language(ext):
    mapping = {
        "py": "python",
        "sql": "mysql",
        "cpp": "cpp",
        "java": "java",
        "c": "c",
        "js": "javascript",
        "ts": "typescript",
        "cs": "csharp",
        "go": "go",
        "rb": "ruby",
        "rs": "rust",
        "kt": "kotlin",
        "swift": "swift",
        "scala": "scala",
        "sh": "bash"
    }
    return mapping.get(ext.lower())

restructure_exports()
