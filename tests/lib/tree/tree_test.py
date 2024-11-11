from lib.tree.node import TreeNode
import lib.tree.utils as tree_utils
import unittest


class TestTreeOperations(unittest.TestCase):
    def setUp(self) -> None:
        # r
        # |__ 1
        # |   |__ 4
        # |   |__ 5
        # |__ 2
        # |__ 3
        #     |__ 6

        root = TreeNode(data="r")
        child_r_1 = TreeNode(parent=root, data="r-1")
        TreeNode(parent=root, data="r-2")
        child_r_3 = TreeNode(parent=root, data="r-3")
        child_1_4 = TreeNode(parent=child_r_1, data="1-4")
        TreeNode(parent=child_r_1, data="1-5")
        TreeNode(parent=child_r_3, data="3-6")
        self.root = root
        self.child_r_3 = child_r_3
        self.child_r_1 = child_r_1
        self.child_1_4 = child_1_4

    def test_tree_construction(self):
        # check len
        self.assertEqual(tree_utils.size(self.root), 7)

    def test_traverse_tree_depth_first(self):
        # collect from 1
        collected_root = [v.data for v in tree_utils.traverse(self.root)]
        self.assertListEqual(
            collected_root, ["r", "r-1", "1-4", "1-5", "r-2", "r-3", "3-6"]
        )

        # collect from 3
        collected_r_3 = [v.data for v in tree_utils.traverse(self.child_r_3)]
        self.assertListEqual(collected_r_3, ["r-3", "3-6"])

    def test_traverse_tree_breadth_first(self):
        # collect from 1
        collected_root = [
            v.data
            for v in tree_utils.traverse(
                self.root, mode=tree_utils.TraversalMode.BREADTH_FIRST
            )
        ]
        self.assertListEqual(
            collected_root, ["r", "r-1", "r-2", "r-3", "1-4", "1-5", "3-6"]
        )

        # collect from 3
        collected_r_3 = [v.data for v in tree_utils.traverse(self.child_r_3)]
        self.assertListEqual(collected_r_3, ["r-3", "3-6"])

    def test_insert_remove_node(self):
        current_size = tree_utils.size(self.root)
        added = TreeNode(data="added", parent=self.root)
        self.assertEqual(current_size + 1, tree_utils.size(self.root))
        added.parent = None
        self.assertEqual(current_size, tree_utils.size(self.root))

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
