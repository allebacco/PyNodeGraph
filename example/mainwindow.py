from PyQt4.Qt import pyqtSlot
from PyQt4.QtGui import QMainWindow, QInputDialog

from node_view import NodeGraphView
from node_item_impl import NodeItemImpl
from connection_item_impl import ConnectionItemImpl
from items.connector_item import InputConnectorItem, OutputConnectorItem


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)

        self._nodeGraph = NodeGraphView()
        self.setCentralWidget(self._nodeGraph)

        menubar = self.menuBar()
        nodeMenu = menubar.addMenu('Graph')
        nodeMenu.addAction('Add node', self.onAddNode)
        nodeMenu.addAction('Add default node', self.addDefaultNode)

        scene = self._nodeGraph.scene()
        scene.sigCreateConnection.connect(self.onAddConnection)

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
        node.setPos(scene.sceneRect().center())
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

    @pyqtSlot()
    def addDefaultNode(self):
        name, ok = QInputDialog.getText(self, 'Add new node', 'Insert the name of the node')
        if not ok:
            return

        name = str(name)
        if len(name) == 0:
            return

        scene = self._nodeGraph.scene()
        node = NodeItemImpl(name)
        scene.addNode(node)
        node.setPos(scene.sceneRect().center())
        node.sigRemove.connect(scene.removeNode)
        node.sigAddConnector.connect(self.onAddConnector)

        node.addConnector(InputConnectorItem('in', ['in_%d' % i for i in xrange(3)]))
        node.addConnector(OutputConnectorItem('out', ['out_%d' % i for i in xrange(3)]))

    @pyqtSlot(str, str)
    def onAddConnection(self, port1Name, port2Name):
        self._nodeGraph.scene().addConnection(port1Name, port2Name, ConnectionItemImpl())

