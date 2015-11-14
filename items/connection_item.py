from PyQt4.Qt import Qt
from PyQt4.QtCore import QPointF
from PyQt4.QtGui import QGraphicsLineItem, QBrush, QColor, QPen, QPainterPath, QGraphicsPathItem


'''
class ConnectionItem(QGraphicsLineItem):

    def __init__(self, parent=None):
        QGraphicsLineItem.__init__(self, parent=parent)

        self._startName = None
        self._endName = None

        brush = QBrush(QColor(Qt.black))

        pen = QPen(brush, 2.0)
        self.setPen(pen)

    def setStart(self, pos):
        line = self.line()
        line.setP1(pos)
        self.setLine(line)

    def setEnd(self, pos):
        line = self.line()
        line.setP2(pos)
        self.setLine(line)
    '''


class ConnectionItem(QGraphicsPathItem):

    def __init__(self, parent=None):
        QGraphicsPathItem.__init__(self, parent=parent)

        self._startName = None
        self._endName = None
        self._path = None

        self._startPos = None
        self._endPos = None

        brush = QBrush(QColor(Qt.black))

        pen = QPen(brush, 2.0)
        self.setPen(pen)

    def setStart(self, pos):
        self._startPos = QPointF(pos)
        self._updatePath()

    def setEnd(self, pos):
        self._endPos = QPointF(pos)
        self._updatePath()

    def _updatePath(self):
        p0 = self._startPos
        p1 = self._endPos
        if p0 is None or p1 is None:
            return

        path = QPainterPath()
        path.moveTo(p0)
        dx = p1.x() - p0.x()
        x0 = p0.x() + 0.7 * dx
        x1 = p1.x() - 0.7 * dx
        path.cubicTo(QPointF(x0, p0.y()), QPointF(x1, p1.y()), p1)
        self.setPath(path)

    def setStartPortName(self, name):
        self._startName = name

    def setEndPortName(self, name):
        self._endName = name

    def name(self):
        return str(self._startName) + '->' + str(self._endName)

    def remove(self):
        self.scene().removeConnection(self._startName, self._endName)
