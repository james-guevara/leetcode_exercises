# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def deepestLeavesSum(self, root: Optional[TreeNode]) -> int:

        queue = deque([root])

        while queue:            

            nodes_in_current_level = len(queue)
            mySum = 0
            currIndex = 0

            for _ in range(nodes_in_current_level):
                node = queue.popleft()
                if node:
                    mySum += node.val
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)

        return mySum


#                if node.left:
#                    if root_flag:
#                        root_flag = False
#                        continue
#                    queue.append(node.left)
#                if node.right:
#                    queue.append(node.right)

