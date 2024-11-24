from binaryninjaui import UIContext

from PySide6.QtCore import QPoint, QRect, QSize
from PySide6.QtGui import QPixmap, QRegion, QImage
from PySide6.QtWidgets import QApplication, QWidget


def _scaledSize(r: QRect, scale: float) -> QSize:
    """
    Get the scaled size of a QRect.

    :param r: the QRect to scale
    :param scale: the scaling factor to use
    :retval: the resulting QSize of the operation
    """

    s = QRect(r)

    s.setWidth(int(r.width() * scale))
    s.setHeight(int(r.height() * scale))

    return s.size()


def renderWidgetImage(widget: QWidget, scale: float) -> QPixmap:
    """
    Get an image (QPixmap) of the given widget. Does not save the image to
    disk; the caller is responsible for saving the image.

    :param scale: the DPI-scaling factor to render the image at
    """

    rect = widget.rect()

    img = QPixmap(_scaledSize(rect, scale))
    img.setDevicePixelRatio(scale)
    widget.render(img, QPoint(), QRegion(rect))

    return img


def renderActiveWindow(scale: float) -> QPixmap:
    """
    Get an image of the main window. Will raise a ValueError if the active
    window could not be found.

    :param scale: the DPI-scaling factor to render the image at
    """

    if (mainWindow := QApplication.activeWindow()) is None:
        raise ValueError("Could not find active window.")

    return renderWidgetImage(mainWindow, scale)


def renderActiveView(scale: float) -> QPixmap:
    """
    Get an image of the currently active linear/graph view. Will raise a
    ValueError if the active view could not be found.

    :param scale: the DPI-scaling factor to render the image at
    """

    uiContext = UIContext.activeContext()
    if uiContext and (viewFrame := uiContext.getCurrentViewFrame()):
        if (view := viewFrame.getCurrentWidget()) is None:
            raise ValueError("Could not find active view via ui context.")
    elif activeWindow := QApplication.activeWindow():
        if (view := activeWindow.childAt(QPoint(150, 150))) is None:
            raise ValueError("Could not find active view via heuristics.")
    else:
        raise ValueError("Could not find active view.")

    return renderWidgetImage(view, scale)


def copyToClipboard(image: QImage) -> None:
    QApplication.clipboard().setImage(image)
