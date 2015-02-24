class node(object):
    def __init__(self, value, children = []):
        self.value = value
        self.children = children
    def __repr__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret
    def walk(node):
        """ iterate tree in pre-order depth-first search order """
        yield node
        for child in node.children:
            for n in walk(child):
                yield n
