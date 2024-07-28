# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
    
import sys    
    

def getMinAndMax(node, currMin, currMax, curr_max_abs_diff):
    
    if not node:
        return (currMin, currMax, curr_max_abs_diff)
    
    if node.val < currMin:
        currMin = node.val
    if node.val > currMax:
        currMax = node.val
    
    xmin, xmax, xmax_abs_diff = getMinAndMax(node.left, currMin, currMax, curr_max_abs_diff)
    ymin, ymax, ymax_abs_diff = getMinAndMax(node.right, currMin, currMax, curr_max_abs_diff)
    
    if xmin < currMin: currMin = xmin
    if xmax > currMax: currMax = xmax 
    if ymin < currMin: currMin = ymin
    if ymax > currMax: currMax = ymax
        
    # now, I can get temporary max absolute difference
    # Compare this node's val to currMin and currMax, and if it's greater than curr_max_abs_diff, 
    # then return it
    a1 = abs(node.val - currMin)
    a2 = abs(node.val - currMax)
    this_max_abs_diff = max(a1, a2)
    
    xy_max = max(xmax_abs_diff, ymax_abs_diff)
    curr_max_abs_diff = max(xy_max, this_max_abs_diff)
    
    
    return (currMin, currMax, curr_max_abs_diff)

class Solution:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:

        
        currMin, currMax, max_abs_diff = getMinAndMax(root, root.val, root.val, 0)
        
        return max_abs_diff

