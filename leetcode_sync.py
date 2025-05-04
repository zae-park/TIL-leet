import os
import requests
from bs4 import BeautifulSoup

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
    'login': 'your_username',  # LeetCode GitHub 로그인 사용자명
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

# 푼 문제 목록 출력
problems = soup.find_all('div', class_='reactable-data')
for problem in problems:
    problem_name = problem.find('a').get_text()
    print(f'Problem: {problem_name}')
