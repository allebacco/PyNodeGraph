from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsEllipseItem, QPen, QBrush, QColor


class CoreItem(QGraphicsEllipseItem):

    def __init__(self, radius, parent=None):
        QGraphicsEllipseItem.__init__(self, QRectF(-radius, -radius, radius*2.0, radius*2.0), parent=parent)

        self._pen = QPen(QColor('#000000'))
        self._pen.setWidth(1)
        self.setPen(self._pen)

        self._hoverPen = QPen(QColor('#000000'))
        self._hoverPen.setWidth(2)

        brush = QBrush(QColor('#FF9966'))
        self.setBrush(brush)

        self._isSelected = False
        self._isHover = False

        self.setAcceptHoverEvents(True)

    def setIsHover(self, isHover):
        self._isHover = isHover
        pen = self._hoverPen if isHover else self._pen
        self.setPen(pen)
        self.update()

    def hoverEnterEvent(self, event):
        QGraphicsEllipseItem.hoverEnterEvent(self, event)
        event.accept()
        self.setIsHover(True)

    def hoverLeaveEvent(self, event):
        QGraphicsEllipseItem.hoverLeaveEvent(self, event)
        event.accept()
        self.setIsHover(False)
