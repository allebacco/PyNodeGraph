from PyQt4.Qt import Qt
from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsItem, QGraphicsObject

from core_component_item import CoreComponentItem
from io_component_item import InputConnector, OutputConnector


class NodeGraphicsItem(QGraphicsObject):

    def __init__(self, name, parent=None):
        QGraphicsObject.__init__(self, parent=parent)

        self._coreItem = CoreComponentItem(40, parent=self)
        self._inputConnector = None
        self._outputConnector = None

        self._isSelected = False
        self._isHover = False
        self.setObjectName(name)

        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def name(self):
        return self.objectName()

    def boundingRect(self):
        return self._coreItem.boundingRect().adjusted(-2, -2, 2, 2)

    def shape(self):
        return self._coreItem.shape()

    def paint(self, painter, option, widget):
        pass

    def hoverEnterEvent(self, event):
        QGraphicsObject.hoverEnterEvent(self, event)
        event.accept()
        self._isHover = True

    def hoverLeaveEvent(self, event):
        QGraphicsObject.hoverLeaveEvent(self, event)
        event.accept()
        self._isHover = False

    def setInputs(self, names):
        inputConn = self._inputConnector

        # Remove previous connector
        if inputConn is not None:
            inputConn.setParentItem(None)
            self.scene().removeItem(inputConn)
        inputConn = None

        if names is not None and len(names) > 0:
            inputConn = InputConnector(names, parent=self)

        self._inputConnector = inputConn

    def setOutputs(self, names):
        outputConn = self._outputConnector

        # Remove previous connector
        if outputConn is not None:
            outputConn.setParentItem(None)
            self.scene().removeItem(outputConn)
        outputConn = None

        if names is not None and len(names) > 0:
            outputConn = OutputConnector(names, parent=self)

        self._outputConnector = outputConn
