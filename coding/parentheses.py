# https://leetcode.com/problems/valid-parentheses/
def isValid(self, s: str) -> bool:
    p = '({['
    m = {')': '(', '}': '{', ']': '['}

    stack = []
    for c in s:
        if c in p:
            stack.append(c)
        else:
            if not stack or stack[-1] != m[c] : return False
            stack.pop()
    return not stack
