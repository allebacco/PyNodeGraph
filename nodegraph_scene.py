from PyQt4.Qt import Qt, pyqtSignal
from PyQt4.QtCore import QLineF
from PyQt4.QtGui import QGraphicsScene

from nodes.io_component_item import IOComponentItem
from nodes.dragged_line_component import DraggedLineComponent


class NodeGraphScene(QGraphicsScene):

    connectionCreationRequest = pyqtSignal(str, str)

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent=parent)

        self._draggedLineItem = None

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
            line = QLineF(pos0, pos1)
            self._draggedLineItem = DraggedLineComponent(line)
            self.addItem(self._draggedLineItem)
        else:
            self._draggedLineItem.setEndpoint(pos1)

        underItems = self.items(pos1)
        vaildItem = None
        for item in underItems:
            if isinstance(item, IOComponentItem) and \
               item.canAcceptConnection(startItem):
                print 'valid'
                vaildItem = item
                break
            else:
                print 'invalid'

        self._draggedLineItem.showEndpoint(vaildItem is not None)

        if done:
            self.removeItem(self._draggedLineItem)
            self._draggedLineItem = None

            if vaildItem is not None:
                # Request connection creation
                name1 = startItem.parentItem().name()
                name2 = vaildItem.parentItem().name()
                self.connectionCreationRequest.emit(name1, name2)
