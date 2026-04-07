import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import *

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

        self.root_browse_button.setFixedWidth(90)
        self.trash_browse_button.setFixedWidth(90)
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
        image_path = self.selected_thumbnail_path

        if image_path and Path(image_path).exists():
            final_path = image_path
        else:
            final_path = self.placeholder_path

        if not final_path or not Path(final_path).exists():
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("No Preview")
            return

        pixmap = QPixmap(str(final_path))
        if pixmap.isNull():
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("No Preview")
            return

        rounded = self.build_rounded_preview(
            pixmap,
            self.PREVIEW_WIDTH,
            self.PREVIEW_HEIGHT,
            self.PREVIEW_RADIUS,
        )
        self.preview_label.setText("")
        self.preview_label.setPixmap(rounded)

    def build_rounded_preview(self, pixmap: QPixmap, width: int, height: int, radius: int) -> QPixmap:
        scaled = pixmap.scaled(
            width,
            height,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )

        result = QPixmap(width, height)
        result.fill(Qt.transparent)

        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing, True)

        path = QPainterPath()
        path.addRoundedRect(0, 0, width, height, radius, radius)
        painter.setClipPath(path)

        x = (scaled.width() - width) // 2
        y = (scaled.height() - height) // 2
        painter.drawPixmap(-x, -y, scaled)
        painter.end()

        return result

    def accept(self) -> None:
        name = self.name_edit.text().strip()
        root = self.root_edit.text().strip().replace("\\", "/")
        trash = self.trash_edit.text().strip().replace("\\", "/")

        if not name:
            QMessageBox.warning(self, "Missing Data", "Project name is required.")
            return

        if not root:
            QMessageBox.warning(self, "Missing Data", "Project root is required.")
            return

        if not os.path.exists(root):
            QMessageBox.warning(self, "Invalid Root", "Project root does not exist.")
            return

        if not trash:
            QMessageBox.warning(self, "Missing Data", "Trash folder is required.")
            return

        if not os.path.exists(trash):
            reply = QMessageBox.question(
                self,
                "Create Trash Folder",
                f"The trash folder does not exist:\n\n{trash}\n\nCreate it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )

            if reply != QMessageBox.Yes:
                return

            try:
                os.makedirs(trash, exist_ok=True)
            except Exception as exc:
                QMessageBox.critical(self, "Error", f"Could not create trash folder:\n{exc}")
                return

        super().accept()

    def get_values(self) -> dict:
        return {
            "name": self.name_edit.text().strip(),
            "root": self.root_edit.text().strip().replace("\\", "/"),
            "trash_dir": self.trash_edit.text().strip().replace("\\", "/"),
            "thumbnail_path": self.selected_thumbnail_path,
        }