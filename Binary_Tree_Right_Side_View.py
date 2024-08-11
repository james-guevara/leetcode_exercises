# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from collections import deque


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        queue = deque([root])
        root_flag = True

        myvals = []

        while queue:            

            nodes_in_current_level = len(queue)
            
            currIndex = 0

            for _ in range(nodes_in_current_level):
                node = queue.popleft()

                currIndex += 1

                if currIndex == nodes_in_current_level:
                    if node:
                        myvals.append(node.val)


                if node:
                    # print(node.val)

                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)

        return myvals


#                if node.left:
#                    if root_flag:
#                        root_flag = False
#                        continue
#                    queue.append(node.left)
#                if node.right:
#                    queue.append(node.right)

