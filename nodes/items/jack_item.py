from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsEllipseItem, QPen, QBrush, QColor


class JackItem(QGraphicsEllipseItem):

    def __init__(self, name, radius, parent=None):
        QGraphicsEllipseItem.__init__(self, QRectF(-radius, -radius, radius*2.0, radius*2.0), parent=parent)

        self._name = name

        pen = QPen(QColor('#000000'))
        pen.setWidth(3)
        self.setPen(pen)

        brush = QBrush(QColor('#000000'))
        self.setBrush(brush)

        self.setToolTip(name)
