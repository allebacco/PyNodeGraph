from PyQt4.Qt import Qt
from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsEllipseItem, QPen, QBrush, QColor


class PortItem(QGraphicsEllipseItem):

    def __init__(self, name, radius, parent=None):
        QGraphicsEllipseItem.__init__(self, QRectF(-radius, -radius, radius*2.0, radius*2.0), parent=parent)

        self._name = name

        #node = self.parentItem()
        #while node.parentItem():
        #    node = node.parentItem()
        self._fullname = parent.fullname() + ':' + name

        #self._nodeItem = node

        pen = QPen(QColor('#000000'))
        pen.setWidth(3)
        self.setPen(pen)

        brush = QBrush(QColor('#000000'))
        self.setBrush(brush)

        self.setToolTip(name)

        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setAcceptHoverEvents(True)

        self._isDraggingLine = False

    def name(self):
        return self._name

    def fullname(self):
        return self._fullname

    def mousePressEvent(self, mouseEvent):
        """Manage the mouse pressing.

        Args:
            event(QMouseEvent): Mouse event.
        """
        mouseEvent.accept()
        self._isDraggingLine = False

    def mouseMoveEvent(self, mouseEvent):
        """Manage the mouse movement while it is pressed.

        Args:
            event(QMouseEvent): Mouse event.
        """
        mouseEvent.accept()
        pos1 = self.scenePos()
        pos2 = mouseEvent.scenePos()
        self.scene().ioLineDrag(self, pos1, pos2, done=False)
        self._isDraggingLine = True

    def mouseReleaseEvent(self, mouseEvent):
        """Manage the mouse releasing.

        Args:
            event(QMouseEvent): Mouse event.
        """
        mouseEvent.accept()
        if self._isDraggingLine:
            pos1 = self.scenePos()
            pos2 = mouseEvent.scenePos()
            self.scene().ioLineDrag(self, pos1, pos2, done=True)

        self._isDraggingLine = False
