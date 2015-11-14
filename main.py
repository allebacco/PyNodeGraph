from PyQt4 import QtGui

from nodegraph_view import NodeGraphView
from items.node_item import NodeItem


def main():
    app = QtGui.QApplication([])
    app.setApplicationName("Test")

    w = NodeGraphView()
    w.setWindowTitle("NodeGraphView - Test")

    scene = w.scene()
    node1 = NodeItem('Node1')
    scene.addItem(node1)
    node1.setPos(20, 30)
    node1.addDefaultInputConnector(['Input11'])
    node1.addDefaultOutputConnector(['Output11', 'Output12'])

    node2 = NodeItem('Node2')
    scene.addItem(node2)
    node2.setPos(160, 180)
    node2.addDefaultInputConnector(['Input21', 'Input22'])
    node2.addDefaultOutputConnector(['Output21', 'Output22', 'Output23'])

    w.resize(800, 600)
    w.show()

    app.exec_()

    # Workaround for GTK assertion fails on exit
    w = None


if __name__ == '__main__':
    main()
