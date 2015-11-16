from PyQt4.Qt import pyqtSlot
from PyQt4.QtGui import QMainWindow, QInputDialog

from nodegraph_view import NodeGraphView
from node_item_impl import NodeItemImpl
from items.connector_item import InputConnectorItem, OutputConnectorItem


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)

        self._nodeGraph = NodeGraphView()
        self.setCentralWidget(self._nodeGraph)

        menubar = self.menuBar()
        nodeMenu = menubar.addMenu('Graph')
        nodeMenu.addAction('Add node', self.onAddNode)

        scene = self._nodeGraph.scene()
        scene.sigCreateConnection.connect(scene.addConnection)

    @pyqtSlot()
    def onAddNode(self):
        name, ok = QInputDialog.getText(self, 'Add new node', 'Insert the name of the node')
        if not ok:
            return

        name = str(name)
        if len(name) == 0:
            return

        scene = self._nodeGraph.scene()
        node = NodeItemImpl(name)
        scene.addNode(node)
        pos = scene.sceneRect().center()
        node.setPos(pos)
        node.sigRemove.connect(scene.removeNode)
        node.sigAddConnector.connect(self.onAddConnector)

    @pyqtSlot(NodeItemImpl)
    def onAddConnector(self, nodeItem):
        name, ok = QInputDialog.getItem(self, 'Add connector', 'Select the type of connector', ['in', 'out'])
        if not ok:
            return
        name = str(name)
        if len(name) == 0:
            return

        numPorts, ok = QInputDialog.getInt(self, 'Add connector', 'Select the number of ports', value=1)
        if not ok or numPorts <= 0:
            return

        ports = ['%s_%d' % (name, i) for i in xrange(numPorts)]

        if name == 'in':
            conn = InputConnectorItem(name, ports)
        else:
            conn = OutputConnectorItem(name, ports)

        nodeItem.addConnector(conn)

