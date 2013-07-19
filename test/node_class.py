class TreeNode(object):
    def __init__(self, name):
        self.children = []
        self.parent = None
        self.name = name
        self.leaf_set = set()
    def add_child(self, node):
        self.children.append(node)
        assert node.parent is None
        node.parent = self


name2node = {} 

for line in tax_file:
	data = (line.split('\t|\t'))
    taxon = TreeNode(data[:3])


#so every node tolweb or otol has the structure of TreeNode objects
#re attributes. does this necessitate some kind of branching structure?
#or should I be able to loop through (?) 


n = 'Pan'
name2node[n] = TreeNode(n)
n = 'Pan troglodytes'
assert n not in name2node
name2node[n] = = TreeNode(n)

