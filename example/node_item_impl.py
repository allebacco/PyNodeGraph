from PyQt4.Qt import pyqtSignal
from PyQt4.QtGui import QMenu

from pynodegraph import NodeItem, IOConnectorItem


class NodeItemImpl(NodeItem):

    sigAddConnector = pyqtSignal(NodeItem)
    sigRemoveConnector = pyqtSignal(IOConnectorItem)

    sigRemove = pyqtSignal(NodeItem)

    def __init__(self, name, parent=None):
        NodeItem.__init__(self, name, parent=parent)

    def contextMenuEvent(self, event):
        event.accept()

        menu = QMenu()
        addConnectorAction = menu.addAction("Add connector")
        removeAction = menu.addAction("Remove")
        selectedAction = menu.exec_(event.screenPos())

        if selectedAction == addConnectorAction:
            self.sigAddConnector.emit(self)
        elif selectedAction == removeAction:
            self.sigRemove.emit(self)
