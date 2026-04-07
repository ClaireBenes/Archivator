import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import *

from ui.utils.image_helper import build_preview_pixmap

class ProjectSettingsDialog(QDialog):
    """
    Dialog used to edit an existing project.

    Responsibilities:
    - Edit project name
    - Edit project root path
    - Edit trash path
    - Preview thumbnail
    - Select or clear thumbnail
    """

    PREVIEW_WIDTH = 300
    PREVIEW_HEIGHT = 170
    PREVIEW_RADIUS = 10

    def __init__(self, project, placeholder_path: str | None = None, parent=None) -> None:
        super().__init__(parent)

        self.project = project
        self.placeholder_path = placeholder_path
        self.selected_thumbnail_path = getattr(project, "thumbnail_path", None)

        self.setWindowTitle(f"Project Settings - {project.name}")
        self.setMinimumWidth(760)

        self.name_edit = QLineEdit(project.name)
        self.root_edit = QLineEdit(project.root)
        self.trash_edit = QLineEdit(project.trash_dir)

        self.root_browse_button = QPushButton("Browse")
        self.trash_browse_button = QPushButton("Browse")
        self.thumb_browse_button = QPushButton("Set Thumbnail")
        self.thumb_clear_button = QPushButton("Clear")

        self.root_browse_button.setFixedWidth(70)
        self.trash_browse_button.setFixedWidth(70)
        self.thumb_clear_button.setFixedWidth(80)

        self.root_browse_button.clicked.connect(self.browse_root)
        self.trash_browse_button.clicked.connect(self.browse_trash)
        self.thumb_browse_button.clicked.connect(self.browse_thumbnail)
        self.thumb_clear_button.clicked.connect(self.clear_thumbnail)

        self.preview_label = QLabel()
        self.preview_label.setFixedSize(self.PREVIEW_WIDTH, self.PREVIEW_HEIGHT)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #2f3136;
                border: 1px solid #4a4d55;
                border-radius: 10px;
            }
        """)

        self.update_preview()

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(12)
        form_layout.setVerticalSpacing(14)

        form_layout.addWidget(QLabel("Project Name"), 0, 0)
        form_layout.addWidget(self.name_edit, 0, 1)

        root_row = QHBoxLayout()
        root_row.setSpacing(8)
        root_row.addWidget(self.root_edit)
        root_row.addWidget(self.root_browse_button)

        form_layout.addWidget(QLabel("Project Root"), 1, 0)
        form_layout.addLayout(root_row, 1, 1)

        trash_row = QHBoxLayout()
        trash_row.setSpacing(8)
        trash_row.addWidget(self.trash_edit)
        trash_row.addWidget(self.trash_browse_button)

        form_layout.addWidget(QLabel("Trash Folder"), 2, 0)
        form_layout.addLayout(trash_row, 2, 1)

        left_panel = QVBoxLayout()
        left_panel.setSpacing(0)
        left_panel.addLayout(form_layout)
        left_panel.addStretch()

        thumb_buttons_row = QHBoxLayout()
        thumb_buttons_row.setSpacing(8)
        thumb_buttons_row.addWidget(self.thumb_browse_button)
        thumb_buttons_row.addWidget(self.thumb_clear_button)
        thumb_buttons_row.addStretch()

        right_panel = QVBoxLayout()
        right_panel.setSpacing(10)
        right_panel.addWidget(QLabel("Thumbnail Preview"))
        right_panel.addWidget(self.preview_label)
        right_panel.addLayout(thumb_buttons_row)
        right_panel.addStretch()

        content_row = QHBoxLayout()
        content_row.setSpacing(24)
        content_row.addLayout(left_panel, 3)
        content_row.addLayout(right_panel, 2)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(18)
        main_layout.addLayout(content_row)
        main_layout.addWidget(self.buttons)

    def browse_root(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Project Root")
        if folder:
            self.root_edit.setText(folder.replace("\\", "/"))

    def browse_trash(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Trash Folder")
        if folder:
            self.trash_edit.setText(folder.replace("\\", "/"))

    def browse_thumbnail(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select Thumbnail",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )
        if filepath:
            self.selected_thumbnail_path = filepath.replace("\\", "/")
            self.update_preview()

    def clear_thumbnail(self) -> None:
        self.selected_thumbnail_path = None
        self.update_preview()

    def update_preview(self) -> None:
        pixmap = build_preview_pixmap(
            image_path=self.selected_thumbnail_path,
            placeholder_path=self.placeholder_path,
            width=self.PREVIEW_WIDTH,
            height=self.PREVIEW_HEIGHT,
            radius=self.PREVIEW_RADIUS,
            corners="all",
        )

        if pixmap is None:
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("No Preview")
            return

        self.preview_label.setText("")
        self.preview_label.setPixmap(pixmap)

    def accept(self) -> None:
        name = self.name_edit.text().strip()
        root = self.root_edit.text().strip().replace("\\", "/")
        trash = self.trash_edit.text().strip().replace("\\", "/")

        if not name:
            QMessageBox.warning(self, "Missing Data", "Project name is required.")
            self.name_edit.setFocus()
            return

        if not root:
            QMessageBox.warning(self, "Missing Data", "Project root is required.")
            self.root_edit.setFocus()
            return

        if not os.path.exists(root):
            QMessageBox.warning(self, "Invalid Root", "Project root does not exist.")
            self.root_edit.setFocus()
            self.root_edit.selectAll()
            return

        if not trash:
            QMessageBox.warning(self, "Missing Data", "Trash folder is required.")
            self.trash_edit.setFocus()
            return

        if not os.path.exists(trash):
            QMessageBox.warning(
                self,
                "Invalid Trash Folder",
                f"The trash folder does not exist:\n\n{trash}\n\n"
                "Please create it manually or choose an existing folder.",
            )
            self.trash_edit.setFocus()
            self.trash_edit.selectAll()
            return

        super().accept()

    def get_values(self) -> dict:
        return {
            "name": self.name_edit.text().strip(),
            "root": self.root_edit.text().strip().replace("\\", "/"),
            "trash_dir": self.trash_edit.text().strip().replace("\\", "/"),
            "thumbnail_path": self.selected_thumbnail_path,
        }