from PyQt4.Qt import Qt
from PyQt4.QtGui import QGraphicsView

from nodegraph_scene import NodeGraphScene


class NodeGraphView(QGraphicsView):
    """Graphics view .
    """

    def __init__(self, tileSource=None, parent=None):
        """Constructor.

        Args:
            tileSource(MapTileSource): Source for the tiles, default `MapTileSourceOSM`.
            parent(QObject): Parent object, default `None`
        """
        QGraphicsView.__init__(self, parent=parent)
        self.setScene(NodeGraphScene())
        self._lastMousePos = None

    def resizeEvent(self, event):
        """Resize the widget. Reimplemented from `QGraphicsView`.

        Resize the `scene`.

        Args:
            event(QResizeEvent): Resize event.
        """
        QGraphicsView.resizeEvent(self, event)
        size = event.size()
        self.scene().setSize(size.width(), size.height())

    '''
    def mousePressEvent(self, event):
        """Manage the mouse pressing.

        Args:
            event(QMouseEvent): Mouse event.
        """
        QGraphicsView.mousePressEvent(self, event)
        if event.buttons() == Qt.LeftButton:
            self._lastMousePos = event.pos()

    def mouseMoveEvent(self, event):
        """Manage the mouse movement while it is pressed.

        Args:
            event(QMouseEvent): Mouse event.
        """
        QGraphicsView.mouseMoveEvent(self, event)
        if event.buttons() == Qt.LeftButton:
            delta = self._lastMousePos - event.pos()
            self._lastMousePos = event.pos()
            self.scene().translate(delta.x(), delta.y())

    def mouseReleaseEvent(self, event):
        """Manage the mouse releasing.

        Args:
            event(QMouseEvent): Mouse event.
        """
        QGraphicsView.mouseReleaseEvent(self, event)
    '''
