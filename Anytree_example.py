# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 19:56:21 2021

@author: mingke.li
"""

from anytree import Node, RenderTree, AnyNode, PreOrderIter
from anytree.search import find

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)

for pre, fill, node in RenderTree(udo):
    print("%s%s" % (pre, node.name))
    
n = Node(1)

root = AnyNode(id="root")

root = Node("root")
s0 = Node("sub0", parent=root)
s0b = Node("sub0B", parent=s0, foo=4, bar=109)
print(RenderTree(root))

s0.parent
root.children
s0b.path
s0b.foo
[node.name for node in PreOrderIter(root)]
find(s0b, lambda node: node.foo < 6)


