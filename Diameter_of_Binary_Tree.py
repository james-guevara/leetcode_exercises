# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

  

class Solution:
    
    def getDepthTuple2(self, node, currMaxDiameter):        
        if not node.left and not node.right:
            return [ [0,0], currMaxDiameter]
        if not node.left:
            right_node = self.getDepthTuple2(node.right, currMaxDiameter + 1)
            z = max(right_node[0]) + 1
            right_max_diam = right_node[1]
            return [ [0, z], right_max_diam]
        if not node.right:
            left_node = self.getDepthTuple2(node.left, currMaxDiameter + 1)
            z = max(left_node[0]) + 1
            left_max_diam = left_node[1]
            return [ [z, 0], left_max_diam]

        
        left_node = self.getDepthTuple2(node.left, currMaxDiameter + 1)
        right_node = self.getDepthTuple2(node.right, currMaxDiameter + 1)
        
        x = max(left_node[0]) + 1
        y = max(right_node[0]) + 1
        
        diams = [left_node[1], right_node[1], currMaxDiameter, x + y]
        
        #x = max(self.getDepthTuple2(node.left, currMaxDiameter)[0]) + 1
        #y = max(self.getDepthTuple2(node.right, currMaxDiameter)[0]) + 1
        list_ = [x,y]
        
        print(node.val)
        print(list_)
        
        #diam = x + y
        #if diam > currMaxDiameter:
        #    currMaxDiameter = diam
        currMaxDiameter = max(diams)
        
        return [ list_, currMaxDiameter ]

    
        
    
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:        
        out_list, max_diam = self.getDepthTuple2(root, 0)
        return max_diam

        #out_list = self.getDepthTuple(root)
        
        # for each subtree, get the max depth on left and right sides
        #print(self.maxDepth(root))
        #return self.maxDepth(root)

