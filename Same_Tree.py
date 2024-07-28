# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


def add_to_tree_list(node, tree_list):
    if not node:
        tree_list.append(None)
        return

    tree_list.append(node.val)

    add_to_tree_list(node.left, tree_list)
    add_to_tree_list(node.right, tree_list)
    return


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:

        tree_list1 = []
        add_to_tree_list(p, tree_list1)

        tree_list2 = []
        add_to_tree_list(q, tree_list2)

        for i, val1 in enumerate(tree_list1):
            val2 = tree_list2[i]
            
            if val1 != val2: return False
        
        return True
