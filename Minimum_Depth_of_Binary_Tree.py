# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


def getMin(node, depth):
    if not node:
        return
    
    left = getMin(node.left, depth + 1)
    right = getMin(node.right, depth + 1)
    
    if not left and not right:
        return depth
    if not left:
        return right
    if not right:
        return left
    return min(left, right)
    

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        
        minVal = getMin(root, 1)
        if not minVal: return 0
        
        return minVal
        

