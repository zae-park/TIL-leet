import os
import subprocess
import requests
from bs4 import BeautifulSoup

# GitHub Secrets에서 세션 쿠키와 토큰을 환경 변수로 받기
LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('CSRF_TOKEN')

if not LEETCODE_SESSION or not CSRF_TOKEN:
    raise RuntimeError("LeetCode session cookie or CSRF token not provided.")


# `leetcode-export` 명령어 실행 예시 (자동화된 풀이 코드 가져오기)
def sync_leetcode_problems():
    # Python, SQL, NoSQL 문제를 가져오기
    categories = ['python', 'mysql', 'nosql']  # 원하는 언어 리스트
    subcategories = ['algorithm/dynamic_programming', 'database/sql', 'database/nosql']

    for category, subcategory in zip(categories, subcategories):
        # 문제 동기화
        command = [
            "leetcode-export",
            "--cookies", f"csrftoken={CSRF_TOKEN};LEETCODE_SESSION={LEETCODE_SESSION}",
            "--only-accepted",
            "--only-last-submission",
            "--problem-folder-name", subcategory
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error occurred while syncing {category}: {result.stderr}")
        else:
            print(f"Successfully synced {category} problems")


# 디렉토리 구조 생성 함수
def create_directory_structure(category, subcategory, difficulty, title_slug, problem_id, problem_name):
    """
    디렉토리 이름 포맷: `root/{category}/{subcategory}/{difficulty}/{problem_id}_{title_slug}`
    """
    directory_name = f"root/{category}/{subcategory}/{difficulty}/{problem_id}_{title_slug}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name


# 문제 설명과 풀이를 저장하는 함수
def save_problem_description_and_solution(problem_name, title_slug, category, subcategory, difficulty):
    """
    문제 설명과 해결책을 해당 디렉토리 구조로 저장
    """
    # 문제 디렉토리 생성
    directory_name = create_directory_structure(category, subcategory, difficulty, title_slug, problem_name,
                                                problem_name)

    # 문제 설명 저장 (description.md)
    problem_description_url = f'https://leetcode.com/problems/{title_slug}/description/'
    description_response = requests.get(problem_description_url)
    description_soup = BeautifulSoup(description_response.text, 'html.parser')
    description_text = description_soup.find('div', class_='content__u3I1').get_text()

    description_path = os.path.join(directory_name, 'description.md')
    with open(description_path, 'w', encoding='utf-8') as f:
        f.write(description_text)

    # 문제 풀이 파일 포맷 (각 언어에 맞는 포맷 사용)
    if category == 'python':
        solution_path = os.path.join(directory_name, 'solution.py')
    elif category == 'mysql':
        solution_path = os.path.join(directory_name, 'solution.sql')
    elif category == 'nosql':
        solution_path = os.path.join(directory_name, 'solution.nosql')
    else:
        solution_path = os.path.join(directory_name, f'solution.{category}')

    # 여기서 사용자가 푼 풀이 코드를 가져와서 solution 파일로 저장합니다.
    os.system(
        f"leetcode-export --cookies 'csrftoken={CSRF_TOKEN};LEETCODE_SESSION={LEETCODE_SESSION}' --only-accepted --only-last-submission --language={category} --problem-folder-name {directory_name}"
    )

    print(f'Problem {problem_name} synchronized in {directory_name}')


# 문제 동기화 실행
sync_leetcode_problems()
