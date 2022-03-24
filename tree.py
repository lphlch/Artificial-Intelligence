import graphviz as gv


class TreeCreator:

    def __init__(self) -> None:
        self.dot = gv.Digraph(comment='Tree',strict=True)

    def test(self):
        self.dot.node('A', '1\n2\n')  # doctest: +NO_EXE
        self.dot.node('B', 'b')
        self.dot.node('L', 'l')
        self.dot.node('E', 'e')

        self.dot.edges(['AB', 'AL', 'BE'])
        self.dot.edge('B', 'L', constraint='false')
        self.dot.edges([])
        self.dot.render('doctest-output/round-table.gv', view=True)

    def addNode(self, label: list) -> None:
        """add a node to the graph

        Args:
            label (list): show in graph
        """
        self.dot.node(str(label),str(label[0:3])+'\n'+str(label[3:6])+'\n'+str(label[6:9]))
        
    def setParent(self, parent: str, child: str) -> None:
        """set the parent of the node

        Args:
            parent (str): parent of the node
            child (str): child of the node
        """
        self.dot.edge(str(parent),str(child))
        

    def create(self) -> None:
        """create the graph
        """
        self.dot.render('img/tree',format="png", view=False)

    def highlightSolutionPath(self, goal) -> None:
        """highlight the solution path

        Args:
            path (list): solution path
        """
        while goal.parent is not None:
            self.dot.edge(str(goal.parent.status),str(goal.status),color='red')
            goal=goal.parent

# t = TreeCreator()
# l=[1,2,3]
# t.addNode(l)
# t.addNode([2,3,4])
# t.setParent(str(l),str([2,3,4]))

# t.show()
