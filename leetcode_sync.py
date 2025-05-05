import os
import subprocess
import requests

# GitHub Secrets에서 세션 쿠키와 토큰을 환경 변수로 받기
LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('CSRF_TOKEN')

if not LEETCODE_SESSION or not CSRF_TOKEN:
    raise RuntimeError("LeetCode session cookie or CSRF token not provided.")


# `leetcode-export` 명령어 실행 예시 (자동화된 풀이 코드 가져오기)
def sync_leetcode_problems():
    languages = ['python', 'mysql', 'pythondata']

    # 각 언어에 대한 디렉토리 생성
    for language in languages:
        language_dir = f"root/{language}"
        if not os.path.exists(language_dir):
            os.makedirs(language_dir)

        os.system(
            f"leetcode-export --cookies 'csrftoken={CSRF_TOKEN};LEETCODE_SESSION={LEETCODE_SESSION}' --only-accepted --only-last-submission --language={language} --problem-folder-name '{language_dir}'")


# 디렉토리 구조 생성 함수
def create_directory_structure(language, difficulty, problem_id, title_slug):
    """
    디렉토리 이름 포맷: `root/{language}/{difficulty}/{problem_id}_{title_slug}`
    """
    directory_name = f"root/{language}/{difficulty}/{problem_id}_{title_slug}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name


def save_problem_description_and_solution(language, difficulty, problem_id, title_slug):
    """
    문제 설명과 해결책을 해당 디렉토리 구조로 저장
    """
    # 문제 디렉토리 생성
    directory_name = create_directory_structure(language, difficulty, problem_id, title_slug)

    # 문제 설명 저장 (description.md)
    problem_description_url = f'https://leetcode.com/problems/{title_slug}/description/'
    description_response = requests.get(problem_description_url)
    description_text = description_response.text  # 텍스트 추출

    description_path = os.path.join(directory_name, 'description.md')
    with open(description_path, 'w', encoding='utf-8') as f:
        f.write(description_text)

    # 문제 풀이 파일 (예: python 문제는 solution.py로 저장)
    solution_path = os.path.join(directory_name, f'solution.{language}')

    # 여기서 사용자가 푼 풀이 코드를 가져와서 solution 파일로 저장
    os.system(
        f"leetcode-export --cookies 'csrftoken={CSRF_TOKEN};LEETCODE_SESSION={LEETCODE_SESSION}' --only-accepted --only-last-submission --language={language} --problem-folder-name {directory_name}")

    print(f'Problem {problem_id} - {title_slug} synchronized in {directory_name}')


# 문제 동기화 실행
sync_leetcode_problems()


# 예시로 각 문제에 대한 메타정보 가져오기
def get_metadata_for_problem(problem_id, title_slug):
    metadata_url = f"https://leetcode.com/api/problems/all/"
    response = requests.get(metadata_url)
    data = response.json()

    for problem in data['stat_status_pairs']:
        if problem['stat']['question_id'] == problem_id:
            difficulty = problem['difficulty']['level']
            return difficulty  # 1: easy, 2: medium, 3: hard
    return 'medium'  # 기본값


# 문제 메타정보 가져오기 및 동기화 실행
def sync_all_problems():
    languages = ['python', 'mysql', 'pythondata']
    for language in languages:
        try:
            problem_list = os.listdir(f"root/{language}")  # 해당 언어의 문제 목록을 가져옴
        except FileNotFoundError:
            print(f"Error: {language} directory not found. Skipping.")
            continue

        for problem in problem_list:
            # 문제 디렉토리 내 파일을 처리하도록 수정 (파일 이름 규칙을 수정할 필요가 있음)
            try:
                # 문제 ID와 제목을 파일명에서 추출하도록 변경
                problem_parts = problem.split('-')
                if len(problem_parts) >= 2:
                    problem_id = problem_parts[0]
                    title_slug = '-'.join(problem_parts[1:])
                    difficulty = get_metadata_for_problem(problem_id, title_slug)
                    save_problem_description_and_solution(language, difficulty, problem_id, title_slug)
                else:
                    print(f"Skipping invalid file name: {problem}")
            except Exception as e:
                print(f"Error processing problem {problem}: {e}")
                continue


# 동기화 실행
sync_all_problems()
