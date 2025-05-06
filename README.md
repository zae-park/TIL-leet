# 🧠 TIL-LeetCode : Sync to GitHub

[LeetCode](https://leetcode.com)에서 푼 문제들을 자동으로 동기화합니다.

> ✅ **매일 자정** GitHub Actions를 통해 자동 실행됩니다.

---

## 🔧  요약

* `leetcode-export` CLI를 활용하여 Accepted 된 문제들만 추출
* 각 문제마다 설명(`description.md`)과 코드(`solution.py`, `solution.sql`, ...)등을 아래의 구조로 정리
* 파일 구조는 **root / 언어 / 문제ID-슬럽** 형태 (아래 디렉토리 구조 참조)
* GitHub Actions를 통해 매일 자정 자동 업데이트

---

## 📁 디렉토리 구조

```
my_solutions/
🔹 python/
🔹🔸 1-two-sum/
       🔹 description.md
       🔹 solution.py
🔹 mysql/
🔹🔸 183-customers-who-never-order/
       🔹 description.md
       🔹 solution.sql
```

* `my_solutions/{language}/{question_id}-{title_slug}/`
* 문제 설명은 `description.md`
* 제출한 코드는 `solution.{확장자}`로 저장

---

## ⚙️ FORK 시 설정 방법

이 레포지토리를 fork하고 아래의 설정을 완료하면 개인 leetcode 싱크 레포지토리로 사용할 수 있습니다.

### 1. 환경 변수 설정

fork한 레포지토리의 Secrets에 다음 값을 등록합니다:

| 이름                 | 설명                           |
| ------------------ | ---------------------------- |
| `LEETCODE_SESSION` | LeetCode 로그인 세션 쿠키           |
| `CSRF_TOKEN`       | LeetCode 요청에 필요한 CSRF 토큰     |
| `LEETCODE_PAT`     | GitHub Personal Access Token |
| `GIT_USER_NAME`    | 커미트 시 사용할 이름                 |
| `GIT_USER_EMAIL`   | 커미트 시 사용할 이메일                |

> 세션/토큰은 [브라우저 개발자 도구(F12)](https://leetcode.com)에서 케이크 값을 확인해서 등록하세요.

---

### 2. GitHub Actions 구성

`root/.github/workflows/leetcode_sync.yml` 추가

```yaml
name: LeetCode Sync

on:
  schedule:
    - cron: "0 0 * * *"  # 매일 자정(UTC) 실행
  workflow_dispatch:     # 수목 실행 가능

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install leetcode-export
        run: pip install leetcode-export

      - name: Run sync script
        run: python leetcode_sync.py
        env:
          LEETCODE_SESSION: ${{ secrets.LEETCODE_SESSION }}
          CSRF_TOKEN: ${{ secrets.CSRF_TOKEN }}

      - name: Commit & Push
        run: |
          git config user.name "${{ secrets.GIT_USER_NAME }}"
          git config user.email "${{ secrets.GIT_USER_EMAIL }}"
          git pull origin main
          git add -A
          if git diff-index --quiet HEAD; then
            echo "No new changes to commit."
          else
            git commit -m "chore: sync LeetCode solutions"
            git push https://x-access-token:${{ secrets.LEETCODE_PAT }}@github.com/${{ github.repository }}.git
```

---

## 📌 Reference

* [`leetcode-export`](https://github.com/clearloop/leetcode-export) 활용
* 문제 설명은 가능한 경우 한국어로 저장
* 문제에 meta.json이 추출되지 않은 경우, solution의 확장자를 기반으로 언어를 추론합니다.
* 풀이된 문제만 가져옵니다!

---

## 🧠 Let's Dig In!

