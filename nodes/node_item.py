from PyQt4.Qt import Qt
from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QGraphicsItem, QGraphicsObject

from items.core_item import CoreItem
from items.connector_item import InputConnectorItem, OutputConnectorItem


class NodeItem(QGraphicsObject):

    def __init__(self, name, parent=None):
        QGraphicsObject.__init__(self, parent=parent)

        self._coreItem = CoreItem(40, parent=self)
        self._inputConnector = None
        self._outputConnector = None

        self._isSelected = False
        self._isHover = False
        self.setObjectName(name)

        self._connectors = dict()

        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemHasNoContents, True)

    def name(self):
        return str(self.objectName())

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
            inputConn = InputConnectorItem('in', names, parent=self)

        self._inputConnector = inputConn
        self._connectors['in'] = inputConn

    def setOutputs(self, names):
        outputConn = self._outputConnector

        # Remove previous connector
        if outputConn is not None:
            outputConn.setParentItem(None)
            self.scene().removeItem(outputConn)
        outputConn = None

        if names is not None and len(names) > 0:
            outputConn = OutputConnectorItem('out', names, parent=self)

        self._outputConnector = outputConn
        self._connectors['out'] = outputConn

    def addConnector(self, connector):
        name = connector.name()
        if name in self._connectors:
            return False

        self._connectors[name] = connector
        return True

    def addConnection(self, portFullname, connection):
        port = portFullname.split(':')
        assert len(port) == 3
        assert port[0] == self.name()
        nodeName = port[0]
        connectorName = port[1]
        portName = port[2]

        connector = self._connectors[connectorName]
        return connector.addConnection(portName, connection)

    def removeConnection(self, portFullname):
        port = portFullname.split(':')
        assert len(port) == 3
        assert port[0] == self.name()
        nodeName = port[0]
        connectorName = port[1]
        portName = port[2]

        connector = self._connectors[connectorName]
        connector.removeConnection(portName)

    def isConnected(self, portFullname):
        port = portFullname.split(':')
        assert len(port) == 3
        assert port[0] == self.name()
        nodeName = port[0]
        connectorName = port[1]
        portName = port[2]

        return self._connectors[connectorName].isConnected(portName)
