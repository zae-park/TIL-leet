import os
import shutil
from pathlib import Path
import json

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

        # 1. meta.json이 있다면 우선 활용
        meta_file = problem_folder / "meta.json"
        if meta_file.exists():
            with open(meta_file, encoding="utf-8") as f:
                meta = json.load(f)
            qid = meta.get("questionFrontendId", "unknown")
            slug = meta.get("titleSlug", problem_folder.name)
            lang = meta.get("lang", "unknown").lower()
        else:
            # meta.json이 없을 경우 폴더명에서 추출
            folder_parts = problem_folder.name.split("-", 1)
            if len(folder_parts) == 2:
                qid, slug = folder_parts
            else:
                slug = problem_folder.name
                qid = "unknown"

        # 2. 코드 파일 자동 감지
        code_file, ext = None, None
        for file in problem_folder.iterdir():
            if file.is_file() and file.name != "description.md" and file.suffix:
                ext_candidate = guess_extension(file.suffix)
                if ext_candidate in extension_to_language_map:
                    code_file = file
                    ext = ext_candidate
                    break

        if not code_file or not ext:
            print(f"Skipping {problem_folder.name}, 코드 파일 추론 실패.")
            continue

        # 언어 확인 또는 추정
        lang = extension_to_language(ext)

        new_path = root_dir / lang / f"{qid}-{slug}"
        new_path.mkdir(parents=True, exist_ok=True)

        # 설명 복사
        if (problem_folder / "description.md").exists():
            shutil.copy(problem_folder / "description.md", new_path / "description.md")
        else:
            print(f"Warning: description.md 없음 → {qid}-{slug}")

        # 코드 복사
        shutil.copy(code_file, new_path / f"solution.{ext}")
        print(f"Saved: {qid}-{slug} ({lang})")

def guess_extension(suffix):
    return suffix.lstrip(".").lower()

extension_to_language_map = {
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

def extension_to_language(ext):
    return extension_to_language_map.get(ext.lower())

restructure_exports()
