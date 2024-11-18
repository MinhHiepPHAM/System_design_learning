
# https://leetcode.com/problems/two-sum/
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seens = {}
        for i, n in enumerate(nums):
            ret = target - n
            if ret in seens: return [seens[ret],i] 
            seens[n] = i
