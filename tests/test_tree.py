import lib.tree.tree as tree
import unittest
from loguru import logger

logger.remove()


class TestTreeOperations(unittest.TestCase):
    def setUp(self) -> None:
        # r
        # |__ 1
        # |   |__ 4
        # |   |__ 5
        # |__ 2
        # |__ 3
        #     |__ 6

        root = tree.TreeNode(data="r")
        child_r_1 = tree.TreeNode(parent=root, data="r-1")
        tree.TreeNode(parent=root, data="r-2")
        child_r_3 = tree.TreeNode(parent=root, data="r-3")
        child_1_4 = tree.TreeNode(parent=child_r_1, data="1-4")
        tree.TreeNode(parent=child_r_1, data="1-5")
        tree.TreeNode(parent=child_r_3, data="3-6")
        self.t = tree.Tree(root=root)
        self.child_r_3 = child_r_3
        self.child_r_1 = child_r_1
        self.child_1_4 = child_1_4
        self.root = root

    def test_tree_construction(self):
        # check len
        self.assertEqual(len(self.t), 7)

    def test_traverse_tree_depth_first(self):
        # collect from 1
        collected_root = [v.data for v in self.t.traverse()]
        self.assertListEqual(
            collected_root, ["r", "r-1", "1-4", "1-5", "r-2", "r-3", "3-6"]
        )

        # collect from 3
        collected_r_3 = [v.data for v in tree.Tree(self.child_r_3).traverse()]
        self.assertListEqual(collected_r_3, ["r-3", "3-6"])

    def test_traverse_tree_breadth_first(self):
        # collect from 1
        collected_root = [
            v.data for v in self.t.traverse(mode=tree.TraversalMode.BREADTH_FIRST)
        ]
        self.assertListEqual(
            collected_root, ["r", "r-1", "r-2", "r-3", "1-4", "1-5", "3-6"]
        )

        # collect from 3
        collected_r_3 = [v.data for v in tree.Tree(self.child_r_3).traverse()]
        self.assertListEqual(collected_r_3, ["r-3", "3-6"])

    def test_insert_remove_node(self):
        current_size = len(self.t)
        added = tree.TreeNode(data="added", parent=self.root)
        self.assertEqual(current_size + 1, len(self.t))
        added.parent = None
        self.assertEqual(current_size, len(self.t))

    def test_get_children(self):
        children_r_1 = [v.data for v in self.child_r_1.children]
        self.assertListEqual(children_r_1, ["1-4", "1-5"])

    def test_loop(self):
        same_v = self.child_r_1
        with self.assertRaises(RuntimeError):
            same_v.parent = self.child_1_4

    def test_is_leaf(self):
        self.assertTrue(self.child_1_4.is_leaf())


if __name__ == "__main__":
    unittest.main()
