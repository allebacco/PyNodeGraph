from PyQt4.Qt import Qt
from PyQt4.QtGui import QGraphicsLineItem, QBrush, QColor, QPen


class ConnectionItem(QGraphicsLineItem):

    def __init__(self, parent=None):
        QGraphicsLineItem.__init__(self, parent=parent)

        brush = QBrush(QColor(Qt.black))
        #self.setBrush(brush)

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
