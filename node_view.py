from PyQt4.Qt import Qt
from PyQt4.QtGui import QGraphicsView

from node_scene import NodeGraphScene


class NodeGraphView(QGraphicsView):
    """Graphics view .
    """

    def __init__(self, scene=None, parent=None):
        """Constructor.

        Args:
            tileSource(MapTileSource): Source for the tiles, default `MapTileSourceOSM`.
            parent(QObject): Parent object, default `None`
        """
        QGraphicsView.__init__(self, parent=parent)

        if scene is None:
            self.setScene(NodeGraphScene())
        else:
            self.setScene(scene)

    def resizeEvent(self, event):
        """Resize the widget. Reimplemented from `QGraphicsView`.

        Resize the `scene`.

        Args:
            event(QResizeEvent): Resize event.
        """
        QGraphicsView.resizeEvent(self, event)
        size = event.size()
        self.scene().setSize(size.width(), size.height())
