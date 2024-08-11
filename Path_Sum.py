# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


def getSum(node, sum_, targetSum):
    if not node: return False # it's a null node, and sum was less than targetSum at this point, so return False

    sum_ += node.val # add this node's value to sum_

    if sum_ == targetSum and (not node.left) and (not node.right): 
        return True # now sum_ could be equal to targetSum, check

    returnVal_l = getSum(node.left, sum_, targetSum) # then get return value from left_side
    returnVal_r = getSum(node.right, sum_, targetSum) # and right side

    if returnVal_l or returnVal_r:
        return True




class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:

        if not root: return False

        sum_ = 0

        result = getSum(root, sum_, targetSum)
        return result
        
