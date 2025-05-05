import os
import subprocess

# GitHub Secrets에서 세션 쿠키와 토큰을 환경 변수로 받기
LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('CSRF_TOKEN')

if not LEETCODE_SESSION or not CSRF_TOKEN:
    raise RuntimeError("LeetCode session cookie or CSRF token not provided.")

root_dir = "my_solutions"
os.makedirs(root_dir)
# `leetcode-export` 명령어 실행 예시 (자동화된 풀이 코드 가져오기)
def sync_leetcode_problems():
    # Python과 SQL 문제만 가져오기
    os.system(f"leetcode-export --cookies 'csrftoken={CSRF_TOKEN};LEETCODE_SESSION={LEETCODE_SESSION}' --only-accepted --only-last-submission --language=python --problem-folder-name '{root_dir}/python'")
    os.system(f"leetcode-export --cookies 'csrftoken={CSRF_TOKEN};LEETCODE_SESSION={LEETCODE_SESSION}' --only-accepted --only-last-submission --language=mysql --problem-folder-name '{root_dir}/mysql'")

# 문제 동기화 실행
sync_leetcode_problems()