from compiler.ast import tree, tree_node
import unittest


class TestTreeOperations(unittest.TestCase):
    def setUp(self) -> None:
        t = tree.Tree()

        # r
        # |__ 1
        # |   |__ 4
        # |   |__ 5
        # |__ 2
        # |__ 3
        #     |__ 6

        root = t.create_node(data="r")
        child_r_1 = t.create_node(parent=root, data="r-1")
        t.create_node(parent=root, data="r-2")
        child_r_3 = t.create_node(parent=root, data="r-3")
        t.create_node(parent=child_r_1, data="1-4")
        t.create_node(parent=child_r_1, data="1-5")
        t.create_node(parent=child_r_3, data="3-6")
        self.t = t
        self.child_r_3 = child_r_3
        self.child_r_1 = child_r_1

    def test_create_node(self):
        # check len
        self.assertEqual(len(self.t), 7)

    def test_traverse_tree_depth_first(self):
        # collect from 1
        collected_root = [v.data for v in self.t.traverse()]
        self.assertListEqual(
            collected_root, ["r", "r-1", "1-4", "1-5", "r-2", "r-3", "3-6"]
        )

        # collect from 3
        collected_r_3 = [v.data for v in self.t.traverse(node=self.child_r_3)]
        self.assertListEqual(
            collected_r_3, ["r-3", "3-6"]
        )  

    def test_traverse_tree_breadth_first(self):
        # collect from 1
        collected_root = [v.data for v in self.t.traverse(mode=tree.Tree.TraversalMode.BREADTH_FIRST)]
        self.assertListEqual(
            collected_root, ["r", "r-1", "r-2", "r-3", "1-4", "1-5", "3-6"]
        )

        # collect from 3
        collected_r_3 = [v.data for v in self.t.traverse(node=self.child_r_3)]
        self.assertListEqual(
            collected_r_3, ["r-3", "3-6"]
        )  

    def test_remove_node(self):
        t = tree.Tree()
        node = tree_node.TreeNode("data=added")
        t.add_node(node)
        count = t.remove_node(node)
        self.assertEqual(count, 1)
        self.assertTrue(node not in t)
        self.assertTrue(len(t) == 0)

    def test_add_node(self):
        t = tree.Tree()
        node = tree_node.TreeNode(data="added")
        t.add_node(node)
        self.assertTrue(node in t)

    def test_contains(self):
        self.assertTrue(self.child_r_1 in self.t)
        self.assertTrue(self.child_r_3 in self.t)

    def test_get_children(self):
        children_r_1 = [v.data for v in self.child_r_1.get_children()]
        self.assertListEqual(children_r_1, ["1-4", "1-5"])

    def atest_remove_invalid_node(self):
        node = tree_node.TreeNode(data="stranger")
        self.assertRaises(ValueError, self.t.remove_node, node)

    def test_traverse_invalid_node(self):
        node = tree_node.TreeNode(data="stranger")
        with self.assertRaises(ValueError):
            [v for v in self.t.traverse(node)]

if __name__ == "__main__":
    unittest.main()
