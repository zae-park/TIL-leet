class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}          # 각 문자의 마지막 위치 기억
        max_len = 0
        start = 0          # 현재 substring의 시작 인덱스

        for i, c in enumerate(s):
            if c in seen and seen[c] >= start:
                # 중복 발생 -> start를 이전 위치 다음으로 이동
                start = seen[c] + 1
            seen[c] = i     # 문자 위치 업데이트
            max_len = max(max_len, i - start + 1)

        return max_len