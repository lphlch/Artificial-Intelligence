import graphviz as gv


class TreeCreator:

    def __init__(self) -> None:
        """initialize
        """
        self.dot = gv.Digraph(comment='Tree', strict=True)

    def addNode(self, sentence) -> None:
        """add a node to the graph

        Args:
            sentence (Sentence): show in graph
        """
        # self.dot.node(sentence.label+'\n'+str(sentence), shape='box')
        self.dot.node(sentence.label, sentence+'\n'+str(sentence), shape='box')

    def setParent(self, parent: str, child: str) -> None:
        """set the parent of the node

        Args:
            parent (str): parent of the node
            child (str): child of the node
        """
        self.dot.edge(str(parent), str(child), shape='box')

    def create(self) -> None:
        """create the graph
        """
        self.dot.render('img/tree', format="png", view=False)

    def clear(self) -> None:
        """clear the graph
        """
        self.dot.clear()

# if __name__ == '__main__':
#     treeCreator = TreeCreator()
#     treeCreator.setParent('a', 'b')
#     treeCreator.create()
# t = TreeCreator()
# l=[1,2,3]
# t.addNode(l)
# t.addNode([2,3,4])
# t.setParent(str(l),str([2,3,4]))

# t.show()
