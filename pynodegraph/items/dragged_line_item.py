from PyQt4.Qt import Qt
from PyQt4.QtCore import QPointF
from PyQt4.QtGui import QGraphicsEllipseItem, QBrush, QColor, QPen, QGraphicsPathItem, QPainterPath


class DraggedLineItem(QGraphicsPathItem):

    def __init__(self, p0, p1, parent=None):
        QGraphicsPathItem.__init__(self, parent=parent)

        self._p0 = p0
        self._p1 = p1

        self._startPoint = QGraphicsEllipseItem(-3, -3, 6, 6, parent=self)
        self._startPoint.setPos(p0)
        self._endPoint = QGraphicsEllipseItem(-3, -3, 6, 6, parent=self)
        self._endPoint.setVisible(False)

        brush = QBrush(QColor(Qt.black))
        self._startPoint.setBrush(brush)
        self._endPoint.setBrush(brush)

        pen = QPen(brush, 2.0)
        self.setPen(pen)

    def showEndpoint(self, show):
        self._endPoint.setVisible(show)

    def setEndpoint(self, pos):
        self._p1 = pos
        self._endPoint.setPos(pos)
        self._updatePath()

    def _updatePath(self):
        p0 = self._p0
        p1 = self._p1

        path = QPainterPath()
        path.moveTo(p0)
        dx = p1.x() - p0.x()
        x0 = p0.x() + 0.7 * dx
        x1 = p1.x() - 0.7 * dx
        path.cubicTo(QPointF(x0, p0.y()), QPointF(x1, p1.y()), p1)
        self.setPath(path)


