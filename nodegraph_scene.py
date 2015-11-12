from PyQt4.Qt import Qt, pyqtSignal, pyqtSlot
from PyQt4.QtCore import QLineF
from PyQt4.QtGui import QGraphicsScene

from nodes.items.port_item import PortItem
from nodes.dragged_line_component import DraggedLineComponent
from nodes.node_item import NodeItem
from nodes.connection_item import ConnectionItem


class NodeGraphScene(QGraphicsScene):

    connectionCreationRequest = pyqtSignal(str, str)

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent=parent)

        self._draggedLineItem = None

        self.connectionCreationRequest.connect(self.onConnectionCreationRequest)

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

    def nodeFromName(self, name):
        for item in self.items():
            if isinstance(item, NodeItem):
                if item.name() == name:
                    return item

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
        line = QLineF(pos0, pos1)
        if self._draggedLineItem is None:
            self._draggedLineItem = DraggedLineComponent(line)
            self.addItem(self._draggedLineItem)
        else:
            self._draggedLineItem.setEndpoint(pos1)

        underItems = self.items(pos1)
        vaildItem = None

        if line.length() > 5.0:
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
                self.connectionCreationRequest.emit(name1, name2)

    @pyqtSlot(str, str)
    def onConnectionCreationRequest(self, port1Name, port2Name):
        port1Name = str(port1Name)
        port2Name = str(port2Name)

        node1Name = port1Name.split(':')[0]
        node2Name = port2Name.split(':')[0]

        node1 = self.nodeFromName(node1Name)
        node2 = self.nodeFromName(node2Name)

        if node1.isConnected(port1Name) or node2.isConnected(port2Name):
            return

        conn = ConnectionItem()
        self.addItem(conn)
        node1.addConnection(port1Name, conn)
        node2.addConnection(port2Name, conn)

        print 'New connection', port1Name, port2Name



