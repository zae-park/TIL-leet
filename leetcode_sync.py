import os
import subprocess

# GitHub Secrets에서 세션 쿠키와 토큰을 환경 변수로 받기
LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('CSRF_TOKEN')

if not LEETCODE_SESSION or not CSRF_TOKEN:
    raise RuntimeError("LeetCode session cookie or CSRF token not provided.")

root_dir = "my_solutions"
if not os.path.exists(root_dir):
    os.makedirs(root_dir)

# `leetcode-export` 명령어 실행 예시 (자동화된 풀이 코드 가져오기)
def sync_leetcode_problems():
    for lang in ["python", "pythondata", "mysql"]:
        dir_path = f"{root_dir}/{lang}"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        os.system(f"leetcode-export --cookies 'csrftoken={CSRF_TOKEN};LEETCODE_SESSION={LEETCODE_SESSION}' --only-accepted --language={lang} --problem-folder-name '{dir_path}'")

# 문제 동기화 실행
sync_leetcode_problems()