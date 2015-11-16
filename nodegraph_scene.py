from PyQt4.Qt import Qt, pyqtSignal, pyqtSlot
from PyQt4.QtCore import QLineF
from PyQt4.QtGui import QGraphicsScene

from items.port_item import PortItem
from items.dragged_line_item import DraggedLineItem
from items.node_item import NodeItem
from items.connection_item import ConnectionItem

from node_utils import nodeNameFromFullname


class NodeGraphScene(QGraphicsScene):

    sigCreateConnection = pyqtSignal(str, str)

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent=parent)

        self._draggedLineItem = None

    @pyqtSlot(NodeItem)
    def addNode(self, nodeItem):
        assert isinstance(nodeItem, NodeItem)
        self.addItem(nodeItem)

    def setSize(self, width, height):
        dw = (width - self.width()) / 2.0
        dh = (height - self.height()) / 2.0
        rect = self.sceneRect()
        rect.adjust(-dw, -dh, dw, dh)
        self.setSceneRect(rect)

    def translate(self, dx, dy):
        rect = self.sceneRect()
        rect.adjust(dx, dy, dx, dy)
        self.setSceneRect(rect)

    def nodeItems(self):
        nodes = list()
        for item in self.items():
            if isinstance(item, NodeItem):
                nodes.append(item)
        return nodes

    def nodeFromName(self, name):
        for item in self.items():
            if isinstance(item, NodeItem):
                if item.name() == name:
                    return item
        return None

    def connectionFromName(self, name):
        for item in self.items():
            if isinstance(item, ConnectionItem):
                if item.name() == name:
                    return item
        return None

    def mousePressEvent(self, mouseEvent):
        """Manage the mouse pressing.

        Args:
            event(QMouseEvent): Mouse event.
        """
        QGraphicsScene.mousePressEvent(self, mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """Manage the mouse movement while it is pressed.

        Args:
            event(QMouseEvent): Mouse event.
        """
        QGraphicsScene.mouseMoveEvent(self, mouseEvent)
        if not mouseEvent.isAccepted() and mouseEvent.buttons() == Qt.LeftButton:
            delta = mouseEvent.lastScreenPos() - mouseEvent.screenPos()
            self.translate(delta.x(), delta.y())

    def mouseReleaseEvent(self, mouseEvent):
        """Manage the mouse releasing.

        Args:
            event(QMouseEvent): Mouse event.
        """
        QGraphicsScene.mouseReleaseEvent(self, mouseEvent)

    def ioLineDrag(self, startItem, pos0, pos1, done=False):
        if self._draggedLineItem is None:
            self._draggedLineItem = DraggedLineItem(pos0, pos1)
            self.addItem(self._draggedLineItem)
        else:
            self._draggedLineItem.setEndpoint(pos1)

        underItems = self.items(pos1)
        vaildItem = None

        if QLineF(pos0, pos1).length() > 5.0:
            # Check if line is over other PortItem
            for item in underItems:
                if isinstance(item, PortItem):
                    vaildItem = item
                    print item.name()
                    break

        self._draggedLineItem.showEndpoint(vaildItem is not None)

        if done:
            self.removeItem(self._draggedLineItem)
            self._draggedLineItem = None

            if vaildItem is not None:
                # Request connection creation
                name1 = startItem.fullname()
                name2 = vaildItem.fullname()
                self.sigCreateConnection.emit(name1, name2)

    @pyqtSlot(str, str)
    def addConnection(self, port1Name, port2Name):
        port1Name = str(port1Name)
        port2Name = str(port2Name)

        node1Name = port1Name.split(':')[0]
        node2Name = port2Name.split(':')[0]

        if node1Name == node2Name:
            raise RuntimeError('%s and %s belong to the same node %s' % (port1Name, port2Name, node1Name))

        node1 = self.nodeFromName(node1Name)
        node2 = self.nodeFromName(node2Name)

        if node1.isConnected(port1Name) or node2.isConnected(port2Name):
            return

        conn = ConnectionItem()
        self.addItem(conn)
        node1.addConnection(port1Name, conn)
        node2.addConnection(port2Name, conn)

        assert conn.startName() is not None
        assert conn.endName() is not None

    @pyqtSlot(str, str)
    def removeConnectionByPortNames(self, startName, endName):
        startName = str(startName)
        endName = str(endName)

        # Disconnect from start port
        nodeName = nodeNameFromFullname(startName)
        node = self.nodeFromName(nodeName)
        node.removeConnectionByPortName(startName)

        # Disconnect from end port
        nodeName = nodeNameFromFullname(endName)
        node = self.nodeFromName(nodeName)
        node.removeConnectionByPortName(endName)

        # Remove connection
        name = str(startName) + '->' + str(endName)
        conn = self.connectionFromName(name)
        self.removeItem(conn)

    @pyqtSlot(ConnectionItem)
    def removeConnection(self, connectionItem):
        assert isinstance(connectionItem, ConnectionItem)
        assert connectionItem.startName() is not None
        assert connectionItem.endName() is not None

        self.removeConnectionByPortNames(connectionItem.startName(), connectionItem.endName())

    @pyqtSlot(NodeItem)
    def removeNode(self, nodeItem):
        assert isinstance(nodeItem, NodeItem)

        # Remove all connectors
        connectorNames = nodeItem.connectorNames()
        for cname in connectorNames:
            conctorItem = nodeItem.connector(cname)

            # Remove all connections
            for connection in conctorItem.connections().values():
                self.removeConnection(connection)

            nodeItem.removeConnector(conctorItem)

        # Remove the node
        self.removeItem(nodeItem)

        print 'Nodes in scene:'
        for item in self.nodeItems():
            print '\t', item.name()
