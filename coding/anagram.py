# https://leetcode.com/problems/valid-anagram/
def isAnagram(self, s: str, t: str) -> bool:
    d = defaultdict(int)
    for c in s:
        d[c] += 1
    for c in t:
        d[c] -= 1

    return not any(v != 0 for v in d.values())
