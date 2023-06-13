""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import TypeVar, Generic
from linked_stack import LinkedStack
from node import TreeNode
import sys


# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BSTInOrderIterator:
    """ 
        In-order iterator for the binary search tree.
        Performs stack-based BST traversal.
    """

    def __init__(self, root: TreeNode[K, I]) -> None:
        """ 
            Iterator initialiser. 

            :param: root - An object of TreeNode

            :pre: None

            :return: None
            
            :complexity: Best/Worst O(1)
        """

        self.stack = LinkedStack()
        self.current = root

    def __iter__(self) -> BSTInOrderIterator:
        """ 
            Standard __iter__() method for initialisers. Returns itself. 

            :param: None

            :pre: None

            :return: BSTInOrderIterator

            :complexity: Best/Worst O(1)
            
        """

        return self

    def __next__(self) -> K:
        """ 
            The main body of the iterator.
            Returns keys of the BST one by one respecting the in-order.

            :param: None

            :pre: None

            :return: The key of the result

            :complexity: Best/Worst O(N), where N is the number of nodes of the tree
        """

        while self.current:
            self.stack.push(self.current)
            self.current = self.current.left

        if self.stack.is_empty():
            raise StopIteration

        result = self.stack.pop()
        self.current = result.right

        return result.key


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree

            :param: None

            :pre: None

            :return: None
            
            :complexity: Best/Worst O(1)
        """

        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty

            :param: None

            :pre: None

            :return: Boolean, return True is the root is None
            
            :complexity: Best/Worst O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """ 
            Returns the number of nodes in the tree. 

            :param: None

            :pre: None

            :return: int - the length of the tree
            
            :complexity: Best/Worst O(1)
        """

        return self.length

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST

            :param: key - the key of the node we want to search

            :pre: None

            :return: bool - True if the key exists

            :complexity: see __getitem__(self, key: K) -> (K, I)
                         Best O(CompK) finds item in root of tree
                         Worst O(CompK * D) item is not found, where D is depth of tree
                         CompK is complexity of comparing the keys
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __iter__(self) -> BSTInOrderIterator:
        """ Create an in-order iterator. """
        return BSTInOrderIterator(self.root)

    def __getitem__(self, key: K) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it

            :param: the key of the node we want to search

            :pre: None

            :return: return the item by the key given

            :complexity: Best O(CompK) finds the item in the root of the tree
                         Worst O(CompK * D) item is not found, where D is the depth of the tree
                         CompK is the complexity of comparing the keys
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        """
            Searches for a node by its key. Passes root node as first node to search from.

            :param: the key of the node we want to search

            :pre: None

            :return: the return value of the aux function

            :complexity: Best O(CompK) when the element is at the root 
                         Worst O(D*CompK), where D is the tree depth
                         CompK is the complexity of comparing the keys        
        """
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Actually searches for a node by its key. Returns the node if found, raises KeyError if not found.

            :param arg1: current - The object of TreeNode

            :param arg2: key - the key of the TreeNode we want to search

            :pre: None

            :return: TreeNode
        
            :complexity: Best O(CompK) when the element is at the root 
                         Worst O(D*CompK), where D is the tree depth
                         CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: empty
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:  # base case: found
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        """
            Attempts to insert item into the tree based on its key. Passes root node as first node to compare with.

            :param arg1: key - The key of the node we are searching

            :param arg2: item - The item of the node we are searching

            :pre: None

            :return: None
        
            :complexity: Best O(CompK) inserts the item into child of root node, CompK is the complexity of comparing the keys
                         Worst O(comp> + comp<) * O(log N) if balanced, O(N)*(Comp< + Comp>) if unbalanced, where N is number of nodes      
        """
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
            Actually inserts an item into the tree, it uses the Key to insert it

            :param arg1: current - The node we want to insert

            :param arg2: key - The key of the node we want to insert

            :param arg3: item - The item of the node we wan to insert

            :pre: None

            :return: TreeNode - the node we are trying to insert

            :complexity: Best O(CompK) inserts the item into child of root node, CompK is the complexity of comparing the keys
                         Worst O(comp> + comp<) * O(log N) if balanced, O(N)*(Comp< + Comp>) if unbalanced, where N is number of nodes

        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        return current

    def __delitem__(self, key: K) -> None:
        """
            :param: the key of the node we want to delete

            :pre: None

            :return: None
        """
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.

            :param arg1: the node we want to delete

            :param arg2: the key of the node we want to delete

            :pre: None

            :return: the node that is deleted

            :complexity: O(D), where D is the depth of the tree
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        return current

    def get_successor(self, current: TreeNode) -> TreeNode:
        """
            Get successor of the current node.
            It should be a node in the subtree rooted at current having the smallest key among all the
            larger keys.
            If no such node exists, then none should be returned.
            
            
            
            Recall that a successor is defined for a sub-tree rooted at a given node as a node having the smallest key 
            in this sub-tree that is still larger than the root's key. In this case, there is no such node for the sub-tree rooted at node 4.
            e.g.
                        15 
                        /\
                      10  20
                     /    / \
                    5    17  25
                   /\
                  1  7
                      \
                       8
            inorder successor of 1 is 5
            successor of 8 is 10
            successor of 15 is 17 
            :param: current (TreeNode)

            :pre: None

            :return: None if there is no such a node having the smallest key in this sub-tree that is still larger than the current's key, else
                     return the node which is in the sub-tree and larger than the current node

            :complexity: O(D), where D is the depth of the tree
        """
        # if current has right child
        if current.right is not None:
            return self.get_minimal(current.right)
    
        else:
            return None

    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
            Get a node having the smallest key in the current sub-tree.

            :param: current (TreeNode)

            :pre: None

            :return: None if current or current.left is None else return the smallest node in the sub-tree

            :complexity: O(D), where D is the depth of the subtree rooted at current
        """
        # loop down to find the leftmost leaf
        while(current is not None and current.left is not None):
            current = current.left
        return current

    def get_maximal(self, current: TreeNode) -> TreeNode:
        """
            Get a node having the largest key in the current sub-tree.

            :param: current (TreeNode)

            :pre: None

            :return: None if current or current.right is None else return the largest node in the sub-tree

            :complexity: O(D), where D is the depth of the subtree rooted at current
        """
        # loop down to find the rightmost leaf
        while(current is not None and current.right is not None):
            current = current.right
        return current


    def is_leaf(self, current: TreeNode) -> bool:
        """
            Simple check whether or not the node is a leaf. 

            :param: the current Node we want to investigate

            :pre: None

            :return: boolean, return True if the current node is leaf node

            :complexity: Best/Worst O(1)
        """
        return current.left is None and current.right is None

    def draw(self, to=sys.stdout):
        """ Draw the tree in the terminal. """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """ Draw a node and then its children. """

        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left,  prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)


        
