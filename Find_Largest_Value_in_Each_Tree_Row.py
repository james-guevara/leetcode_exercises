from collections import deque


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def largestValues(self, root: Optional[TreeNode]) -> List[int]:
        queue = deque([root])
        mymaxvals = []

        while queue:            
            nodes_in_current_level = len(queue)
            currIndex = 0
            these_vals = []
            for _ in range(nodes_in_current_level):
                
                node = queue.popleft()

                currIndex += 1

                if currIndex == nodes_in_current_level:
                    if node:
                        these_vals.append(node.val)
                        maxval = max(these_vals)
                        mymaxvals.append(maxval)

                if node:
                    these_vals.append(node.val)

                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)

        return mymaxvals


#                if node.left:
#                    if root_flag:
#                        root_flag = False
#                        continue
#                    queue.append(node.left)
#                if node.right:
#                    queue.append(node.right)


