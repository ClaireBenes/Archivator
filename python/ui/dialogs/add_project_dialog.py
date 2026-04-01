import os

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)


class AddProjectDialog(QDialog):
    """
    Dialog used to register a new project.

    Responsibilities:
    - Ask for a project root path
    - Ask for a trash directory
    - Validate paths
    - Ask to create trash folder if missing
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Add Project")
        self.setMinimumWidth(500)

        self.root_edit = QLineEdit()
        self.root_edit.setPlaceholderText("Project root path")

        self.trash_edit = QLineEdit()
        self.trash_edit.setPlaceholderText("Trash path")

        self.root_button = QPushButton("Browse Root")
        self.trash_button = QPushButton("Browse Trash")

        self.root_button.clicked.connect(self.browse_root)
        self.trash_button.clicked.connect(self.browse_trash)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Project Root"))
        layout.addWidget(self.root_edit)
        layout.addWidget(self.root_button)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Trash Folder"))
        layout.addWidget(self.trash_edit)
        layout.addWidget(self.trash_button)
        layout.addSpacing(12)
        layout.addWidget(self.buttons)

    def browse_root(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Project Root")
        if not folder:
            return

        self.root_edit.setText(folder)

        if not self.trash_edit.text().strip():
            self.trash_edit.setText(os.path.join(folder, "01_Trash"))

    def browse_trash(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Trash Folder")
        if folder:
            self.trash_edit.setText(folder)

    def accept(self) -> None:
        """
        Validate inputs before closing dialog.
        """
        root = self.root_edit.text().strip()
        trash = self.trash_edit.text().strip()

        if not root:
            QMessageBox.warning(self, "Missing Data", "Project root is required.")
            return

        if not os.path.exists(root):
            QMessageBox.warning(self, "Invalid Root", "Project root does not exist.")
            return

        if not trash:
            QMessageBox.warning(self, "Missing Trash", "Trash directory is required.")
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
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create trash folder:\n{e}")
                return

        super().accept()

    def get_values(self) -> tuple[str, str]:
        root = self.root_edit.text().strip()
        trash = self.trash_edit.text().strip()
        return root, trash