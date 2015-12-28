from PyQt4.QtGui import QMenu
from pynodeview import ConnectionItem


class ConnectionItemImpl(ConnectionItem):

    def __init__(self, parent=None):
        ConnectionItem.__init__(self, parent=parent)

    def contextMenuEvent(self, event):
        event.accept()

        menu = QMenu()
        removeAction = menu.addAction("Remove")
        selectedAction = menu.exec_(event.screenPos())

        if selectedAction == removeAction:
            self.scene().removeConnection(self)
