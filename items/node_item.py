from PyQt4.Qt import Qt
from PyQt4.QtGui import QGraphicsItem, QGraphicsObject

from core_item import CoreItem
from connector_item import InputConnectorItem, OutputConnectorItem, IOConnectorItem
from node_utils import getItemNames


class NodeItem(QGraphicsObject):

    def __init__(self, name, parent=None):
        QGraphicsObject.__init__(self, parent=parent)

        self._coreItem = CoreItem(40, parent=self)

        self._isSelected = False
        self._isHover = False
        self.setObjectName(name)

        self._connectors = dict()

        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemHasNoContents, True)

        self.setToolTip(name)

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

    def addDefaultInputConnector(self, names):
        inputConn = self._connectors.get('in', None)
        if inputConn is not None:
            raise RuntimeError('Connector in is already present')

        inputConn = InputConnectorItem('in', names)
        self.addConnector(inputConn)

    def addDefaultOutputConnector(self, names):
        outputConn = self._connectors.get('out', None)
        if outputConn is not None:
            raise RuntimeError('Connector out is already present')

        outputConn = OutputConnectorItem('out', names)
        self.addConnector(outputConn)

    def addConnector(self, connector):
        name = connector.name()
        if name in self._connectors:
            raise RuntimeError('Connector %s is already present' % name)

        connector.setParentItem(self)
        self._connectors[name] = connector

        if __debug__:
            for port in connector._ports.itervalues():
                port._fullname.startswith(self.name())

    def addConnection(self, portFullname, connection):
        print portFullname
        nodeName, connectorName, portName = getItemNames(portFullname)
        assert nodeName == self.name()
        assert connectorName in self._connectors
        assert portName in self._connectors[connectorName]._ports

        connector = self._connectors[connectorName]
        return connector.addConnection(portName, connection)

    def connector(self, name):
        return self._connectors[name]

    def connectorNames(self):
        return self._connectors.keys()

    def removeConnector(self, connector):
        name = connector.name()
        if name not in self._connectors:
            raise ValueError('Node has no connector %s' % name)
        numConnections = connector.connectionCount()
        if numConnections > 0:
            return RuntimeError('Connector %s has %s connections' % (name, numConnections))

        connector.setParentItem(None)
        self.scene().removeItem(connector)
        del self._connectors[name]

    def removeConnection(self, connectionItem):
        assert isinstance(connectionItem, IOConnectorItem)
        ok = False
        for connector in self._connectors.itervalues():
            ok = connector.removeConnection(connectionItem)
            if ok:
                return

        raise RuntimeError('Unable to remove connection %s' % connectionItem.name())

    def removeConnectionByPortName(self, portFullname):
        assert isinstance(portFullname, str)

        print portFullname
        nodeName, connectorName, portName = getItemNames(portFullname)

        if self.name() != nodeName:
            raise RuntimeError('%s and %s are not the same node' % (self.name(), nodeName))
        if connectorName not in self._connectors:
            raise RuntimeError('Node %s does not have connector %s' % (nodeName, connectorName))

        connector = self._connectors[connectorName]
        connector.removeConnectionByPortName(portName)

    def isConnected(self, portFullname):
        port = portFullname.split(':')

        assert len(port) == 3

        connectorName = port[1]

        assert port[0] == self.name()
        assert connectorName in self._connectors.iterkeys()

        portName = port[2]
        return self._connectors[connectorName].isConnected(portName)
