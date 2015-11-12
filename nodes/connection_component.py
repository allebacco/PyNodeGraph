from PyQt4.Qt import Qt
from PyQt4.QtGui import QGraphicsLineItem, QBrush, QColor, QPen


class ConnectionComponent(QGraphicsLineItem):

    def __init__(self, nodeFrom, nodeTo, parent=None):
        QGraphicsLineItem.__init__(self, parent=parent)

        brush = QBrush(QColor(Qt.black))
        self._startPoint.setBrush(brush)
        self._endPoint.setBrush(brush)

        pen = QPen(brush, 2.0)
        self.setPen(pen)

    def moveStart(self, dx, dy):
        pass

    def moveEnd(self, dx, dy):
        pass
