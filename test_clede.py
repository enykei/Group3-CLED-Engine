import random
import unittest
from clede import BST

MAP = ["ROAD A B 2", "ROAD B C 3", "ROAD A C 8", "ROAD C D 2", "ROAD B D 7"]   # reference map

def balanced(n):
    if not n:
        return True
    return abs((n.l.h if n.l else 0) - (n.r.h if n.r else 0)) <= 1 and balanced(n.l) and balanced(n.r)


class TestBST(unittest.TestCase):
    def build(self, avl=False):
        t = BST(avl)
        for k in ["P4", "P2", "P6", "P1", "P3", "P5", "P7"]:
            t.insert(k, k.lower())
        return t

    def test_empty_and_duplicate(self):
        t = BST()
        self.assertIsNone(t.find("P1"))
        self.assertIsNone(t.delete("P1"))
        self.assertTrue(t.insert("P1", "a"))
        self.assertFalse(t.insert("P1", "b"))
        self.assertEqual(t.find("P1"), "a")

    def test_delete_cases(self):
        t = self.build()
        self.assertEqual(t.delete("P1"), "leaf")
        self.assertEqual(t.delete("P2"), "one-child")
        self.assertEqual(t.delete("P4"), "two-child")
        self.assertEqual([k for k, _ in t.inorder()], ["P3", "P5", "P6", "P7"])
        self.assertIsNone(t.find("P4"))
        self.assertIsNone(t.delete("P4"))

    def test_plain_bst_not_balanced(self):
        t = BST()
        for k in ["P1", "P2", "P3", "P4"]:
            t.insert(k, 0)
        self.assertEqual(t.rot, []) 
        self.assertFalse(balanced(t.root))


class TestAVL(unittest.TestCase):
    def test_four_rotation_cases(self):
        for keys, rot, root in [(["P1", "P2", "P3"], ["L@P1"], "P2"),
                                (["P3", "P2", "P1"], ["R@P3"], "P2"),
                                (["P3", "P1", "P2"], ["L@P1", "R@P3"], "P2"),
                                (["P1", "P3", "P2"], ["R@P3", "L@P1"], "P2")]:
            t = BST(True)
            for k in keys:
                t.insert(k, 0)
            self.assertEqual(t.rot, rot)
            self.assertEqual(t.root.k, root)

    def test_stress_insert_delete_stays_balanced(self):
        rnd = random.Random(7)
        keys = ["K%03d" % i for i in range(300)]
        rnd.shuffle(keys)
        t = BST(True)
        for k in keys:
            self.assertTrue(t.insert(k, 1))
            self.assertTrue(balanced(t.root))
        rnd.shuffle(keys)
        for k in keys[:200]:
            self.assertIsNotNone(t.delete(k))
            self.assertTrue(balanced(t.root))
        left = sorted(keys[200:])
        self.assertEqual([k for k, _ in t.inorder()], left)

if __name__ == "__main__":
    unittest.main(verbosity=2)