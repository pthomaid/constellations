
class Ducttape:
    """
    Stores data items under paths that look like (a/b/c/d/...)
    Contains functions to get and set data
    """

    def __init__(self):
        self.root = {}

    # path looks like: a/b/c/d/...
    def setitem(self, path, item):
        pa = path.split('/')
        node = self.root
        for i in range(0, len(pa)-1):
            if pa[i] in node:
                if not isinstance(node[pa[i]], dict):
                    node[pa[i]] = {}
                    node = node[pa[i]]
                else:
                    node = node[pa[i]]
            else:
                node[pa[i]] = {}
                node = node[pa[i]]

        node[pa[-1]] = item

    # path looks like: a/b/c/d/...
    def getitem(self, path):
        pa = path.split('/')

        node = self.root
        for p in pa:
            if p in node:
                node = node[p]

        return node

if __name__ == '__main__':
    dt = Ducttape()
    path1 = 'a/b/c'
    dt.setitem(path1, 1)
    path2 = 'a/b/c/d'
    dt.setitem(path2, 2)
    path3 = 'a/b/d/e'
    dt.setitem(path3, 3)

    print(dt.root)
    print(dt.getitem(path1))
    print(dt.getitem(path2))
    print(dt.getitem(path3))
