import sys

class Err(Exception):
    """A user-facing error (bad input,illegal transition, etc)"""

class Node:
    def __init__(self, k, v):
        self.k, self.v, self.l, self.r, self.h = k, v, None, None, 1

def _h(n):
    return n.h if n else 0

class BST:
    def __init__(self, avl=False):
        self.root, self.avl, self.rot = None, avl, []   

    def _node(self, k):
        n = self.root
        while n and n.k != k:
            n = n.l if k < n.k else n.r
        return n

    def find(self, k):
        n = self._node(k)
        return n.v if n else None

    def insert(self, k, v):
        if self._node(k):
            return False
        self.root = self._ins(self.root, k, v)
        return True

    def delete(self, k):
        # handling three cases: leaf, one child, two children
        n = self._node(k)
        if not n:
            return None
        case = "two-child" if n.l and n.r else "one-child" if n.l or n.r else "leaf"
        self.root = self._del(self.root, k)
        return case

    def _ins(self, n, k, v):
        if not n:
            return Node(k, v)
        if k < n.k:
            n.l = self._ins(n.l, k, v)
        else:
            n.r = self._ins(n.r, k, v)
        return self._fix(n)

    def _del(self, n, k):
        if k < n.k:
            n.l = self._del(n.l, k)
        elif k > n.k:
            n.r = self._del(n.r, k)
        else:
            if not n.l:
                return n.r
            if not n.r:
                return n.l
            m = n.r
            while m.l:
                m = m.l
            n.k, n.v = m.k, m.v
            n.r = self._del(n.r, m.k)
        return self._fix(n)

    def _rot(self, n, d):
        self.rot.append("%s@%s" % (d, n.k))
        if d == "R":
            c = n.l; n.l = c.r; c.r = n
        else:
            c = n.r; n.r = c.l; c.l = n
        n.h = 1 + max(_h(n.l), _h(n.r))
        c.h = 1 + max(_h(c.l), _h(c.r))
        return c

    def _fix(self, n):
        n.h = 1 + max(_h(n.l), _h(n.r))
        if self.avl:
            b = _h(n.l) - _h(n.r)
            if b > 1:
                if _h(n.l.l) < _h(n.l.r):
                    n.l = self._rot(n.l, "L")
                n = self._rot(n, "R")
            elif b < -1:
                if _h(n.r.r) < _h(n.r.l):
                    n.r = self._rot(n.r, "R")
                n = self._rot(n, "L")
        return n

    def inorder(self):
        out = []

        def walk(n):
            if n:
                walk(n.l); out.append((n.k, n.v)); walk(n.r)
        walk(self.root)
        return out

    def show(self):
        def f(n):
            if not n:
                return "."
            return n.k if not n.l and not n.r else "(%s %s %s)" % (f(n.l), n.k, f(n.r))
        return f(self.root)