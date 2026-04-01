from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QMenu, QVBoxLayout

from ui.widgets.add_project_card import CARD_WIDTH, CARD_HEIGHT, PREVIEW_HEIGHT


class ProjectCard(QFrame):
    """
    Visual representation of a project.

    Responsibilities:
    - Display project thumbnail area and name
    - Show a context menu on right click
    - Delegate actions back to the main window
    """

    def __init__(self, project, controller, parent=None) -> None:
        super().__init__(parent)

        self.project = project
        self.controller = controller

        self.setObjectName("projectCard")
        self.setFixedSize(CARD_WIDTH, CARD_HEIGHT)

        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
        QFrame#projectCard {
            border: 1px solid #555;
            border-radius: 10px;
            background-color: #313131;
        }
        QFrame#projectCard:hover {
            border: 1px solid #c38b59;
        }
        QLabel {
            color: white;
            background: transparent;
        }
        """)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.preview = QLabel("")
        self.preview.setFixedHeight(PREVIEW_HEIGHT)
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setStyleSheet("""
        background-color: #3a3a3a;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        """)

        info = QFrame()
        info.setStyleSheet("""
        background-color: #2b2b2b;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
        """)

        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(10, 8, 10, 8)

        self.name_label = QLabel(project.name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(self.name_label)

        root_layout.addWidget(self.preview)
        root_layout.addWidget(info)

    def contextMenuEvent(self, event) -> None:
        """
        Show the project context menu on right click.
        """
        menu = QMenu(self)

        trash_menu = menu.addMenu("Trash")
        open_trash_action = trash_menu.addAction("Open Trash Folder")
        empty_action = trash_menu.addAction("Empty Trash")

        settings_action = menu.addAction("Project Settings")
        menu.addSeparator()
        remove_action = menu.addAction("Remove Project")

        action = menu.exec(event.globalPos())

        if action == open_trash_action:
            self.controller.open_project_trash(self.project)
        elif action == empty_action:
            self.controller.empty_project_trash(self.project)
        elif action == settings_action:
            self.controller.open_project_settings(self.project)
        elif action == remove_action:
            self.controller.remove_project(self.project)

    def mousePressEvent(self, event) -> None:
        """
        Open the project when the card is double-clicked.
        """
        if event.button() == Qt.LeftButton:
            self.controller.open_project(self.project)

        super().mousePressEvent(event)