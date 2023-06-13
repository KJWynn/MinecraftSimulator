""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev, with edits by Jackson Goerner'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic, List
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ 
        Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree

            :param: None

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is
            not None. Otherwise, return 0.

            :param arg1: current node to get its height (AVLTreeNode)

            :pre: None

            :return: height of node (int)

            :complexity: Best/Worst O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.

            :param arg1: current node to get its balance factor (AVLTreeNode)

            :pre: None

            :return: balance factor of current node (int)

            :complexity: Best/Worst O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Actually inserts an item into the tree, it uses the Key to insert it.
            Perform rebalancing to ensure invariant is maintained after insertion.

            :param arg1: current node in tree (AVLTreeNode)
            :param arg2: key of node to insert (K)
            :param arg3: item of node to insert (I)

            :pre: None

            :return: new root of subtree (AVLTreeNode)

            :complexity: Best O(CompK) inserts the item into child of root node, CompK is the complexity of comparing the keys
                         Worst O(comp> + comp<) * O(log N), where N is number of nodes

        """

        # Perform normal search on BST
        if current is None:
            # base case at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
        elif key > current.key:
            # link to right edge for larger key
            current.right = self.insert_aux(current.right, key, item)
        elif key < current.key:
            # link to left edge for smaller key
            current.left = self.insert_aux(current.left, key, item)
        else:
            # raise ValueError when duplicated keys detected
            raise ValueError(f"Duplicating item {item} for insertion.")

        # Update height of ancestor node for current node
        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1

        # Update size of current node
        current.size = self.size(current)

        # Call rebalance function to balance the tree if needed
        return self.rebalance(current)
        
        
    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
            Performs rebalancing after deletion to ensure invariant is maintained.

            :param arg1: current node in tree (AVLTreeNode)
            :param arg2: key of node to delete (K)

            :pre: None

            :return: new root of subtree (AVLTreeNode)

            :complexity: Best/Worst O(log N), where N is the total number of nodes of the tree
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key: do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case: find successor, then swap places
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

            # Update the size for successor node
            current.size = self.size(current)

        # Update height of ancestor node for current node
        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1

        # Call rebalance function to balance the tree if needed
        return self.rebalance(current)

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            
            :param arg1: current node in tree (AVLTreeNode)

            :pre: Current node and its right child is not None

            :return: new root of subtree (AVLTreeNode)

            :complexity: Best/Worst O(1)
        """
        # check precondition where current and its right child is not None
        if current is None or current.right is None :
            raise ValueError("Current and child should not be None")

        # Get the links of current root
        child = current.right
        center = child.left

        # Rotate
        child.left = current
        current.right = center

        # Update height of rotated nodes
        current.height = max(self.get_height(current.left),self.get_height(current.right)) + 1
        child.height = max(self.get_height(child.left),self.get_height(child.right)) + 1
        
        # Update size of nodes after rotation
        child.size = self.size(child)
        current.size = self.size(current)

        # Update new root as child after rotation
        return self.rebalance(child)  


    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :param arg1: current node in tree (AVLTreeNode)

            :pre: Current node and its right child is not None

            :return: new root of subtree (AVLTreeNode)

            :complexity: Best/Worst O(1)
        """
        # check precondition where current and its left child is not None
        if current is None or current.left is None :
            raise ValueError("Current and child should not be None")

        # Get the links of current root
        child = current.left
        center = child.right

        # Rotate
        child.right = current
        current.left = center

        # Update height of rotated nodes
        child.height = max(self.get_height(child.left),self.get_height(child.right)) + 1
        current.height = max(self.get_height(current.left),self.get_height(current.right)) + 1

        # Update size of nodes after rotation
        child.size = self.size(child)
        current.size = self.size(current)

        # Update new root as child after rotation
        return self.rebalance(child)


    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.

            :param arg1: current node in tree (AVLTreeNode)

            :pre: None

            :return: new root of subtree (AVLTreeNode)

            :complexity: Best/Worst O(1)
        """
        current.size = self.size(current)

        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    
    def range_between(self, i: int, j: int) -> list:
        """
        Returns a sorted list of all elements in the tree between the ith and jth indices, inclusive.

        :param arg1: ith index to get the elements (int)
        :param arg2: jth index to get the elements (int)

        :pre: k >= j, and that they are in range of 0 to N-1, where N is the total number of nodes in the tree

        :post: List class object should be returned

        :return: sorted list of items in the tree between ith and jth indices inclusive (List)

        :complexity: Best/Worst O(j-i*log(N)), where N is the total number of nodes in the tree.
        
        """
        #check precondition
        try:
            N = self.size(self.root)
            assert (i >= 0 and i <= N+1) and (j >= 0 and j <= N+1) and j>=i, f"i and j should be in range 0 to N-1, where N is the number of nodes in tree, current N is {N}"
        except AssertionError as e:
            raise ValueError(e)
        
        res =  self.range_aux(self.root, i, j)  # call the range_aux method for recursive searching and result

        # check postcondition
        if not isinstance(res,list):
            raise Exception(f"Object of list class is not returned")
        return res

    
    def range_aux(self, current: AVLTreeNode, i: int, j: int, res: list|None = None) -> list:
        """
        Auxillary function for range_between, attemps to add items within ith to jth range inclusive.
        Calls the recursive method to lookup for index-th item in tree.

        :param arg1: ith index to get the elements (int)
        :param arg2: jth index to get the elements (int)

        :pre: None

        :return: sorted list of items in the tree between ith and jth indices inclusive (List)

        :complexity: Best/Worst O(j-i*log(N)), where N is the total number of nodes in the tree
        
        """

        if res is None:
            res = []
        if current is None or i > j:
            return res
        else:
            node = self.lookup(self.root, i)
            res.append(node.item)
            return self.range_aux(self.root, i+1,j,res)


    def lookup(self, node: AVLTreeNode, index: int) -> AVLTreeNode:
        """
        Returns the node at position index in the AVLTree. Searches the index-th item recursively.

        :param arg1: current node in tree (AVLTreeNode)
        :param arg1: index of item to get (int)

        :pre: None

        :return: node at i-th index (AVLTreeNode)

        :complexity: O(log N), where N is the number of nodes in the AVLTree, since it is a balanced binary search tree.

        """
        if index == self.size(node.left):   # return node when found
            return node
        elif index < self.size(node.left):  #  lookup the index-th element in left subtree
            return self.lookup(node.left, index)
        else:                               # lookup the (index-left subtree size - 1)th element in the right subtree
            return self.lookup(node.right, index - self.size(node.left) - 1)
        

    def size(self, current: AVLTreeNode) -> int:
        """
        Update and returns the size of the tree with current node as the "root".
        In general: size of tree = size of left subtree + size of right subtree + 1 (size of "root")

        :param arg1: current node in tree (AVLTreeNode)

        :pre: None

        :return: size of current node (int)

        :complexity: O(1), since it access the attributes of the nodes, assuming that we ignore comparison complexity.

        """
        if current is None:         # return 0 when current is not a node
            return 0

        if self.is_leaf(current):   # update current size as 1 when current is leaf
            current.size = 1
        elif current.left is None:  # update current size as right child size + 1 when there is no left child
            current.size = current.right.size + 1
        elif current.right is None: # update current size as left child size + 1 when there is no right child
            current.size = current.left.size + 1
        else:                       # update current size as left and right child size + 1
            current.size = current.left.size + current.right.size + 1

        return current.size     # returns the size of current node
