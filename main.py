from PyQt4 import QtGui

from nodegraph_view import NodeGraphView
from nodes.node_item import NodeItem


def main():
    app = QtGui.QApplication([])
    app.setApplicationName("Test")

    w = NodeGraphView()
    w.setWindowTitle("NodeGraphView - Test")

    scene = w.scene()
    node1 = NodeItem('Node1')
    scene.addItem(node1)
    node1.setPos(20, 30)
    node1.setInputs(['Input11'])
    node1.setOutputs(['Output11', 'Output12'])

    node2 = NodeItem('Node2')
    scene.addItem(node2)
    node2.setPos(160, 180)
    node2.setInputs(['Input21', 'Input22'])
    node2.setOutputs(['Output21', 'Output22', 'Output23'])

    w.resize(800, 600)
    w.show()

    app.exec_()


if __name__ == '__main__':
    main()
