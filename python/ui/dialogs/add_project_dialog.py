import os

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class AddProjectDialog(QDialog):
    """
    Dialog used to register a new project.

    Responsibilities:
    - Ask for a project root path
    - Ask for a trash directory
    - Return validated user input to the caller
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Add Project")
        self.setMinimumWidth(500)

        self.root_edit = QLineEdit()
        self.root_edit.setPlaceholderText("Project root path")

        self.trash_edit = QLineEdit()
        self.trash_edit.setPlaceholderText("Trash path (optional)")

        self.root_button = QPushButton("Browse Root")
        self.trash_button = QPushButton("Browse Trash")

        self.root_button.clicked.connect(self.browse_root)
        self.trash_button.clicked.connect(self.browse_trash)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Project Root"))
        layout.addWidget(self.root_edit)
        layout.addWidget(self.root_button)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Trash Folder"))
        layout.addWidget(self.trash_edit)
        layout.addWidget(self.trash_button)
        layout.addSpacing(12)
        layout.addWidget(buttons)

    def browse_root(self) -> None:
        """
        Let the user select the project root folder.
        """
        folder = QFileDialog.getExistingDirectory(self, "Select Project Root")
        if not folder:
            return

        self.root_edit.setText(folder)

        if not self.trash_edit.text().strip():
            self.trash_edit.setText(os.path.join(folder, "01_Trash"))

    def browse_trash(self) -> None:
        """
        Let the user select the trash folder.
        """
        folder = QFileDialog.getExistingDirectory(self, "Select Trash Folder")
        if folder:
            self.trash_edit.setText(folder)

    def get_values(self) -> tuple[str, str]:
        """
        Return the entered root path and trash path.

        Returns:
            tuple[str, str]: (root_path, trash_path)
        """
        root = self.root_edit.text().strip()
        trash = self.trash_edit.text().strip()

        if root and not trash:
            trash = os.path.join(root, "01_Trash")

        return root, trash