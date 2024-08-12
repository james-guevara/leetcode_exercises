# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        
        if not root:
            return []
        
        queue = deque([root])
        
        my_vals = []
        zig = False
        
        while queue:
            
            nodes_in_queue = len(queue)
            
            currIndex = 0            
            zig = ~zig
            these_vals = []
            these_vals_x = []
            
            for _ in range(nodes_in_queue):
                node = queue.popleft()
                currIndex += 1
                
                if node:
                    these_vals.append(node.val)
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
                
                if currIndex == nodes_in_queue:
                    if zig:
                        my_vals.append(these_vals)
                    else:
                        while these_vals:
                            these_vals_x.append(these_vals.pop())
                        
                        my_vals.append(these_vals_x)
                    

        return my_vals

