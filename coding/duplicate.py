# https://leetcode.com/problems/contains-duplicate/
def containsDuplicate(self, nums: List[int]) -> bool:
    return len(nums) != len(set(nums))
