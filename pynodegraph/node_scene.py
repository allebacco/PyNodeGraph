from PyQt4.Qt import Qt, pyqtSignal, pyqtSlot
from PyQt4.QtCore import QLineF, QPointF
from PyQt4.QtGui import QGraphicsScene

from items.port_item import PortItem
from items.dragged_line_item import DraggedLineItem
from items.node_item import NodeItem
from items.connection_item import ConnectionItem

from node_utils import nodeNameFromFullname


class NodeGraphScene(QGraphicsScene):
    """Graphicsscene for the nodes

    Attributes:
        _draggedLineItem(DraggedLineItem): Line to draw during the creation of a new connection
    """

    sigCreateConnection = pyqtSignal(str, str)

    def __init__(self, parent=None):
        """Constructor

        Args:
            parent(QObject): Parent object, default None
        """
        QGraphicsScene.__init__(self, parent=parent)

        self._draggedLineItem = None

    @pyqtSlot(NodeItem)
    def addNode(self, nodeItem):
        """Add a node to the scene.

        Args:
            nodeItem(NodeItem): Node to add to the scene
        """
        assert isinstance(nodeItem, NodeItem)
        self.addItem(nodeItem)

    @pyqtSlot(float, float)
    def setSize(self, width, height):
        """Resize the scene

        The size of the scene must be the same of the size of the graphicsview

        Args:
            width(float): New width of the scene
            height(float): New height of the scene
        """
        dw = (width - self.width()) / 2.0
        dh = (height - self.height()) / 2.0
        rect = self.sceneRect()
        rect.adjust(-dw, -dh, dw, dh)
        self.setSceneRect(rect)

    @pyqtSlot(float, float)
    def translate(self, dx, dy):
        """Translate the scene

        Args:
            dx(float): Positive for moving to the right
            dy(float): Positive for moving to the bottom
        """
        rect = self.sceneRect()
        rect.adjust(dx, dy, dx, dy)
        self.setSceneRect(rect)

    def nodeItems(self):
        """List of all the nodes in the scene

        Returns:
            The list of all the NodeItems in the scene
        """
        nodes = list()
        for item in self.items():
            if isinstance(item, NodeItem):
                nodes.append(item)
        return nodes

    def nodeFromName(self, name):
        """Search a node with a particular name

        Args:
            name(str): Name of the node to search

        Returns:
            NodeItem named name or None if no NodeItem is found
        """
        for item in self.items():
            if isinstance(item, NodeItem):
                if item.name() == name:
                    return item
        return None

    def connectionFromName(self, name):
        """Search a node with name

        Args:
            name(str): Name of the connection to search

        Returns:
            ConnectionItem named name or None if no ConnectionItem is found
        """
        for item in self.items():
            if isinstance(item, ConnectionItem):
                if item.name() == name:
                    return item
        return None

    # def mousePressEvent(self, mouseEvent):
    #     """Manage the mouse pressing.
    #
    #     Args:
    #         event(QMouseEvent): Mouse event.
    #     """
    #     QGraphicsScene.mousePressEvent(self, mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """Manage the mouse movement while it is pressed.

        Args:
            event(QMouseEvent): Mouse event.
        """
        QGraphicsScene.mouseMoveEvent(self, mouseEvent)
        if not mouseEvent.isAccepted() and mouseEvent.buttons() == Qt.LeftButton:
            delta = mouseEvent.lastScreenPos() - mouseEvent.screenPos()
            self.translate(delta.x(), delta.y())

    # def mouseReleaseEvent(self, mouseEvent):
    #     """Manage the mouse releasing.
    #
    #     Args:
    #         event(QMouseEvent): Mouse event.
    #     """
    #     QGraphicsScene.mouseReleaseEvent(self, mouseEvent)

    def ioLineDrag(self, startItem, pos0, pos1, done=False):
        """Drag connection line for creating a new connection

        Args:
            startItem(PortItem): PortItem that is the origin of the line
            pos0(QPointF): Coordinates of the origin of the line
            pos1(QPointF): Coordinates of the end of the line
            done(bool): True for indicating the attempt for connection, False
                        for continue dragging

        Emits:
            sigCreateConnection(str, str): Attempt for a connection when done is True
                                           and a PortItem is in the pos1 position.
                                           The receiver of this signal must check if the
                                           connection is really possible
        """
        assert isinstance(startItem, PortItem)
        assert isinstance(pos0, QPointF)
        assert isinstance(pos1, QPointF)
        assert isinstance(done, bool)

        if self._draggedLineItem is None:
            self._draggedLineItem = DraggedLineItem(pos0, pos1)
            self.addItem(self._draggedLineItem)
        else:
            self._draggedLineItem.setEndpoint(pos1)

        vaildItem = None

        if QLineF(pos0, pos1).length() > 5.0:
            # Check if line is over other PortItem
            for item in self.items(pos1):
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

    @pyqtSlot(str, str, ConnectionItem)
    def addConnection(self, port1Name, port2Name, connItem):
        """Add a connection between two PortItems

        The connection is done only if the ports do not belongs to the same node
        and they are not already connected.

        Args:
            port1Name(str): Fullname of the start port
            port2Name(str): Fullname of the end port
            connItem(ConnectionItem): ConnectionItem to use for the connection

        Returns:
            True if the connection is done or False otherwise
        """
        assert isinstance(connItem, ConnectionItem)

        # Ensure port1Name and port2Name are str, not QString
        port1Name = str(port1Name)
        port2Name = str(port2Name)

        node1Name = port1Name.split(':')[0]
        node2Name = port2Name.split(':')[0]

        if node1Name == node2Name:
            return False

        node1 = self.nodeFromName(node1Name)
        node2 = self.nodeFromName(node2Name)

        if node1.isConnected(port1Name) or node2.isConnected(port2Name):
            return False

        self.addItem(connItem)
        node1.addConnection(port1Name, connItem)
        node2.addConnection(port2Name, connItem)

        assert connItem.startPortName() is not None
        assert connItem.endPortName() is not None
        return True

    @pyqtSlot(str, str)
    def removeConnectionByPortNames(self, startName, endName):
        """Remove a connection between two ports

        Args:
            startName(str): Fullname of the start port
            endName(str): Fullname of the end port
        """
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
        name = startName + '->' + endName
        conn = self.connectionFromName(name)
        self.removeItem(conn)

    @pyqtSlot(ConnectionItem)
    def removeConnection(self, connectionItem):
        """Remove a connection

        The connection must exists in the scene

        Args:
            connectionItem(ConnectionItem): Connection to remove
        """
        assert isinstance(connectionItem, ConnectionItem)
        assert connectionItem.startPortName() is not None
        assert connectionItem.endPortName() is not None

        self.removeConnectionByPortNames(connectionItem.startPortName(),
                                         connectionItem.endPortName())

    @pyqtSlot(NodeItem)
    def removeNode(self, nodeItem):
        """Remove anode from the scene

        All the connections to and from the item will be removed

        Args:
            nodeItem(NodeItem): NodeItem to remove.
        """
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
