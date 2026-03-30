from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtWidgets import QLayout, QLayoutItem, QFrame, QMenu



class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, hspacing=20, vspacing=20):
        super().__init__(parent)
        self._items = []
        self._hspacing = hspacing
        self._vspacing = vspacing
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item: QLayoutItem):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def horizontalSpacing(self):
        return self._hspacing

    def verticalSpacing(self):
        return self._vspacing

    def _do_layout(self, rect, test_only=False):
        x = rect.x()
        y = rect.y()
        line_height = 0

        for item in self._items:
            widget = item.widget()
            space_x = self.horizontalSpacing()
            space_y = self.verticalSpacing()
            item_size = item.sizeHint()

            next_x = x + item_size.width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item_size.width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item_size))

            x = next_x
            line_height = max(line_height, item_size.height())

        return y + line_height - rect.y()


class ProjectCard(QFrame):
    def __init__(self, project, app):
        super().__init__()
        self.project = project
        self.app = app
        self.setObjectName("projectCard")
        self.setFixedSize(260, 180)

        self.setStyleSheet("""
        QFrame#projectCard {
            background-color: #2a2c30;
            border: 1px solid #44474f;
            border-radius: 12px;
        }
        QFrame#projectCard:hover {
            border: 1px solid #c38b59;
        }
        """)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        open_action = menu.addAction("Open Project Folder")
        empty_action = menu.addAction("Empty Trash")
        settings_action = menu.addAction("Project Settings")
        remove_action = menu.addAction("Remove Project")

        action = menu.exec(event.globalPos())

        if action == open_action:
            self.app.open_project(self.project)
        elif action == empty_action:
            self.app.empty_project_trash(self.project.id)
        elif action == settings_action:
            self.app.open_project_settings(self.project)
        elif action == remove_action:
            self.app.remove_project(self.project)