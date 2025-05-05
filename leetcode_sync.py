import os
import requests
from bs4 import BeautifulSoup
import json
import re

# GitHub Secrets에서 세션 쿠키와 토큰을 환경 변수로 받기
LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')
if not LEETCODE_SESSION:
    raise RuntimeError("LeetCode session cookie not provided.")

# LeetCode 로그인 URL
leetcode_login_url = 'https://leetcode.com/accounts/login/'

# 세션 시작
session = requests.Session()
login_page = session.get(leetcode_login_url)

# CSRF 토큰 추출
soup = BeautifulSoup(login_page.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

# 로그인 POST 요청 데이터 (세션 쿠키 사용)
login_payload = {
    'csrfmiddlewaretoken': csrf_token,
    'login': 'zae-park',  # LeetCode GitHub 로그인 사용자명
    'password': LEETCODE_SESSION  # LeetCode 세션 쿠키를 비밀번호로 사용
}

# 로그인 요청
login_response = session.post(leetcode_login_url, data=login_payload, headers={'Referer': leetcode_login_url})

if login_response.status_code == 200:
    print("LeetCode 로그인 성공!")
else:
    print("LeetCode 로그인 실패!")

# 푼 문제 목록 페이지 접근
problem_url = 'https://leetcode.com/problemset/all/'
response = session.get(problem_url)
soup = BeautifulSoup(response.text, 'html.parser')


# 디렉토리 구조 생성 함수
def create_directory_structure(language, difficulty, title_slug, problem_id, problem_name):
    # 디렉토리 이름 포맷: `root-{language}-{difficulty}-{problem_id}_{problem_name}`
    directory_name = f"root-{language}-{difficulty}-{problem_id}_{title_slug}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name


# 문제 동기화
problems = soup.find_all('div', class_='reactable-data')
for problem in problems:
    # 문제 정보 추출
    problem_name = problem.find('a').get_text()
    title_slug = problem.find('a').get('href').split('/')[-2]  # 제목 슬러그 (slug)
    problem_id = problem.get('data-id')
    language = problem.get('data-lang')
    difficulty = problem.get('data-difficulty')

    # 언어 필터 (Python 및 SQL 문제만 가져오기)
    if language not in ['python', 'mysql']:  # python과 mysql만 가져옴
        continue

    # 문제 디렉토리 생성
    directory_name = create_directory_structure(language, difficulty, title_slug, problem_id, problem_name)

    # 문제 설명 저장 (description.md)
    problem_description_url = f'https://leetcode.com/problems/{title_slug}/description/'
    description_response = session.get(problem_description_url)
    description_soup = BeautifulSoup(description_response.text, 'html.parser')
    description_text = description_soup.find('div', class_='content__u3I1').get_text()

    description_path = os.path.join(directory_name, 'description.md')
    with open(description_path, 'w', encoding='utf-8') as f:
        f.write(description_text)

    # 문제 풀이 파일 (예: python 문제는 solution.py로 저장)
    if language == 'python':
        solution_path = os.path.join(directory_name, 'solution.py')
    elif language == 'mysql':
        solution_path = os.path.join(directory_name, 'solution.sql')

    # 여기서 사용자가 푼 풀이 코드를 가져와서 solution 파일로 저장합니다.
    # 이를 위해서는 `leetcode-export` 명령어로 풀이 코드를 가져와야 합니다.
    # 예시로 `leetcode-export` 명령어를 통해 자동으로 풀이를 가져오고 저장하도록 합니다.

    # `leetcode-export` 명령어 실행 예시 (자동화된 풀이 코드 가져오기)
    os.system(
        f"leetcode-export --cookies 'csrftoken={os.getenv('CSRF_TOKEN')};LEETCODE_SESSION={os.getenv('LEETCODE_SESSION')}' --only-accepted --only-last-submission --language={language} --problem-folder-name {directory_name}")

    print(f'Problem {problem_name} synchronized in {directory_name}')
