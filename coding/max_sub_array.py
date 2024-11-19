# https://leetcode.com/problems/maximum-subarray/
def maxSubArray(self, nums: List[int]) -> int:
    max_sum = nums[0]
    cur_sum = 0
    for n in nums:
        if cur_sum < 0:
            # reset the cur_sum to get new sub that can increase the max sum
            cur_sum = 0
        cur_sum += n
        if max_sum < cur_sum: max_sum = cur_sum

    return max_sum
