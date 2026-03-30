import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *

from ui.widgets import FlowLayout, ProjectCard

# --------------------------------------------------
# Make root importable
# --------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.registry import ProjectRegistry
from services.archive_service import ArchiveService
from core.exceptions import ArchivatorError


# --------------------------------------------------
# Add Project Dialog
# --------------------------------------------------
class AddProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Project")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        self.root_edit = QLineEdit()
        self.root_edit.setPlaceholderText("Project root path")

        self.trash_edit = QLineEdit()
        self.trash_edit.setPlaceholderText("Trash path (optional)")

        root_btn = QPushButton("Browse Root")
        trash_btn = QPushButton("Browse Trash")

        root_btn.clicked.connect(self.browse_root)
        trash_btn.clicked.connect(self.browse_trash)

        layout.addWidget(QLabel("Project Root"))
        layout.addWidget(self.root_edit)
        layout.addWidget(root_btn)

        layout.addSpacing(10)

        layout.addWidget(QLabel("Trash Folder"))
        layout.addWidget(self.trash_edit)
        layout.addWidget(trash_btn)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addSpacing(12)
        layout.addWidget(buttons)

    def browse_root(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Root")
        if folder:
            self.root_edit.setText(folder)
            if not self.trash_edit.text():
                # your example uses 01_Trash, so keep that as default
                self.trash_edit.setText(os.path.join(folder, "01_Trash"))

    def browse_trash(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Trash Folder")
        if folder:
            self.trash_edit.setText(folder)

    def get_values(self):
        root = self.root_edit.text().strip()
        trash = self.trash_edit.text().strip()

        if root and not trash:
            trash = os.path.join(root, "01_Trash")

        return root, trash


# --------------------------------------------------
# Main App
# --------------------------------------------------
class ArchivatorApp:
    """
    GUI entry point.

    Responsibilities:
    - Display project tiles
    - Show Add Project tile first
    - Call ArchiveService only
    """

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.ui_path = ROOT / "ui" / "view" / "interface.ui"
        self.config_path = ROOT / "config" / "projects.json"

        self.registry = ProjectRegistry(str(self.config_path))
        self.registry.load()
        self.service = ArchiveService(self.registry)

        self.window = self._load_ui()
        self._bind_widgets()
        self._connect_signals()
        self.refresh_projects()

    def _load_ui(self):
        loader = QUiLoader()
        window = loader.load(str(self.ui_path))
        if window is None:
            raise RuntimeError(f"Could not load UI: {self.ui_path}")
        return window

    def _bind_widgets(self):
        self.project_container = self.window.findChild(QWidget, "projectContainer")
        self.search_bar = self.window.findChild(QLineEdit, "searchLineEdit")
        self.settings_button = self.window.findChild(QPushButton, "settingsButton")
        self.sort_combo = self.window.findChild(QComboBox, "sortComboBox")
        self.stats_label = self.window.findChild(QLabel, "statsLabel")

        if self.project_container is None:
            raise RuntimeError("Missing widget 'projectContainer' in interface.ui")

        # Clear any old layout if needed
        old_layout = self.project_container.layout()
        if old_layout is not None:
            QWidget().setLayout(old_layout)

        outer_layout = QVBoxLayout(self.project_container)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.cards_widget = QWidget()
        self.flow_layout = FlowLayout(self.cards_widget, margin=0, hspacing=24, vspacing=24)
        self.cards_widget.setLayout(self.flow_layout)

        self.scroll_area.setWidget(self.cards_widget)
        outer_layout.addWidget(self.scroll_area)

    def _connect_signals(self):
        if self.search_bar is not None:
            self.search_bar.textChanged.connect(self.refresh_projects)

    def clear_grid(self):
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def refresh_projects(self):
        self.clear_grid()

        search_text = ""
        if self.search_bar is not None:
            search_text = self.search_bar.text().strip().lower()

        projects = self.service.list_projects()

        if self.stats_label:
            self.stats_label.setText(f"{len(projects)} projects registered")

        if search_text:
            projects = [
                p for p in projects
                if search_text in p.name.lower()
                   or search_text in p.root.lower()
                   or search_text in p.id.lower()
            ]

        self.flow_layout.addWidget(self.create_add_project_card())

        for project in projects:
            self.flow_layout.addWidget(self.create_project_card(project))

    # --------------------------------------------------
    # Cards
    # --------------------------------------------------
    def create_add_project_card(self):
        card = QFrame()
        card.setObjectName("addProjectCard")
        card.setFixedSize(260, 180)
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet("""
            QFrame#addProjectCard {
                border: 1px solid #555;
                border-radius: 10px;
                background-color: #2b2b2b;
            }
            QFrame#addProjectCard:hover {
                border: 1px solid #888;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setAlignment(Qt.AlignCenter)

        plus = QLabel("+")
        plus.setAlignment(Qt.AlignCenter)
        plus.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")

        text = QLabel("Add Project")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")

        layout.addStretch()
        layout.addWidget(plus)
        layout.addWidget(text)
        layout.addStretch()

        card.mousePressEvent = lambda event: self.add_project()
        return card

    def create_project_card(self, project):
        card = ProjectCard(project, self)
        card.setObjectName("projectCard")
        card.setFixedSize(260, 180)
        card.setStyleSheet("""
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

        root_layout = QVBoxLayout(card)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Full thumbnail preview area
        preview = QLabel("")
        preview.setMinimumHeight(120)
        preview.setAlignment(Qt.AlignCenter)
        preview.setStyleSheet("""
            background-color: #3a3a3a;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)

        # Bottom info area
        info = QFrame()
        info.setStyleSheet("""
            background-color: #2b2b2b;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)

        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(10, 8, 10, 8)
        info_layout.setSpacing(4)

        name_label = QLabel(project.name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        info_layout.addWidget(name_label)

        root_layout.addWidget(preview)
        root_layout.addWidget(info)

        return card

    # --------------------------------------------------
    # Actions
    # --------------------------------------------------
    def add_project(self):
        dialog = AddProjectDialog(self.window)
        if dialog.exec() != QDialog.Accepted:
            return

        root_path, trash_dir = dialog.get_values()

        if not root_path:
            QMessageBox.warning(self.window, "Missing data", "Project root is required.")
            return

        try:
            self.service.add_project(root_path, trash_dir)
            self.refresh_projects()

        except ArchivatorError as e:
            QMessageBox.warning(self.window, "Archivator Error", str(e))
        except Exception as e:
            QMessageBox.critical(self.window, "Unexpected Error", str(e))

    def show_project_menu(self, project, button):
        menu = QMenu(self.window)

        empty_action = menu.addAction("Empty Trash")
        settings_action = menu.addAction("Project Settings")

        action = menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

        if action == empty_action:
            self.empty_project_trash(project.id)
        elif action == settings_action:
            self.open_project_settings(project)

    def empty_project_trash(self, project_id):
        reply = QMessageBox.question(
            self.window,
            "Confirm",
            f"Empty trash for project:\n{project_id} ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            self.service.empty_project_trash(project_id)
            QMessageBox.information(self.window, "Done", "Trash emptied.")
        except ArchivatorError as e:
            QMessageBox.warning(self.window, "Archivator Error", str(e))
        except Exception as e:
            QMessageBox.critical(self.window, "Unexpected Error", str(e))

    def open_project_settings(self, project):
        QMessageBox.information(
            self.window,
            "Project Settings",
            f"Here you can later edit settings for:\n\n{project.name}\n\n"
            f"Root: {project.root}\nTrash: {project.trash_dir}"
        )

    def run(self):
        self.window.show()
        return self.app.exec()


def main():
    gui = ArchivatorApp()
    sys.exit(gui.run())


if __name__ == "__main__":
    main()