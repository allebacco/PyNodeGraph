from PyQt4.Qt import Qt
from PyQt4.QtGui import QGraphicsLineItem, QGraphicsEllipseItem, QBrush, QColor, QPen


class DraggedLineComponent(QGraphicsLineItem):

    def __init__(self, line, parent=None):
        QGraphicsLineItem.__init__(self, line, parent=parent)

        self._startPoint = QGraphicsEllipseItem(-3, -3, 6, 6, parent=self)
        self._startPoint.setPos(line.p1())
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
        line = self.line()
        line.setP2(pos)
        self._endPoint.setPos(pos)
        self.setLine(line)

